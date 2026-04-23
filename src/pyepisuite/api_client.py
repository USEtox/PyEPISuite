import atexit
import os
import queue
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm

from .models import Identifiers


DEFAULT_REMOTE_BASE_URL = 'https://episuite.dev/EpiWebSuite/api'
DEFAULT_LOCAL_STARTUP_TIMEOUT = 60
DEFAULT_JAR_DOWNLOAD_URL = 'https://episuite.dev/api/download'


def _is_cas_formatted(cas: str) -> bool:
    return bool(re.match(r'^(\d{2,7})-(\d{2})-(\d)$', cas))


def _normalize_cas_for_local(cas: str) -> str:
    """Normalize CAS to local DB format where prefix is usually zero-padded."""
    match = re.match(r'^(\d{1,7})-(\d{2})-(\d)$', cas)
    if not match:
        return cas
    first, middle, last = match.groups()
    width = max(6, len(first))
    return f'{first.zfill(width)}-{middle}-{last}'


def _with_api_suffix(base_url: str) -> str:
    cleaned = base_url.rstrip('/')
    if cleaned.endswith('/api'):
        return cleaned
    return f'{cleaned}/api'


class _LocalRuntimeManager:
    _lock = threading.Lock()
    _process = None
    _base_url = None
    _startup_log = []
    _atexit_registered = False

    @classmethod
    def _reader_loop(cls, stream, out_queue):
        try:
            for line in iter(stream.readline, ''):
                if not line:
                    break
                out_queue.put(line)
        finally:
            try:
                stream.close()
            except Exception:
                pass

    @classmethod
    def _extract_base_url(cls, line: str) -> Optional[str]:
        match = re.search(r'EPISuite started on (https?://[^\s]+)', line)
        if not match:
            return None
        return match.group(1).rstrip('/')

    @classmethod
    def _is_alive(cls) -> bool:
        if cls._process is None:
            return False
        return cls._process.poll() is None and cls._base_url is not None

    @classmethod
    def _resolve_jar_path(cls) -> Optional[Path]:
        env_jar = os.getenv('PYEPISUITE_LOCAL_JAR_PATH')
        if env_jar:
            path = Path(env_jar).expanduser().resolve()
            return path if path.exists() else None

        candidates = [
            Path(__file__).resolve().parents[2] / 'data' / 'local' / 'EpiSuiteCLI.jar',
            Path.cwd() / 'data' / 'local' / 'EpiSuiteCLI.jar',
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    @classmethod
    def _download_jar(cls) -> Path:
        dest = Path(__file__).resolve().parents[2] / 'data' / 'local' / 'EpiSuiteCLI.jar'
        dest.parent.mkdir(parents=True, exist_ok=True)
        url = os.getenv('PYEPISUITE_JAR_DOWNLOAD_URL', DEFAULT_JAR_DOWNLOAD_URL)
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0)) or None
        tmp = dest.with_suffix('.jar.tmp')
        try:
            with tmp.open('wb') as fh, tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc='Downloading EpiSuiteCLI.jar',
            ) as progress:
                for chunk in response.iter_content(chunk_size=4 * 1024 * 1024):
                    if chunk:
                        fh.write(chunk)
                        progress.update(len(chunk))
            tmp.replace(dest)
        except Exception:
            tmp.unlink(missing_ok=True)
            raise
        return dest

    @classmethod
    def has_local_assets(cls) -> bool:
        return cls._resolve_jar_path() is not None

    @classmethod
    def ensure_started(cls) -> str:
        with cls._lock:
            if cls._is_alive():
                return cls._base_url

            jar_path = cls._resolve_jar_path()
            if jar_path is None:
                jar_path = cls._download_jar()

            timeout_seconds = int(os.getenv('PYEPISUITE_LOCAL_STARTUP_TIMEOUT', DEFAULT_LOCAL_STARTUP_TIMEOUT))
            cmd = ['java', '-jar', str(jar_path)]

            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
            except FileNotFoundError as exc:
                raise RuntimeError(
                    'Java runtime not found in PATH. Install Java and retry local mode, '
                    'or set PYEPISUITE_MODE=remote.'
                ) from exc

            out_queue: queue.Queue[str] = queue.Queue()
            reader = threading.Thread(
                target=cls._reader_loop,
                args=(process.stdout, out_queue),
                daemon=True,
            )
            reader.start()

            deadline = time.time() + timeout_seconds
            base_url = None
            startup_log = []

            while time.time() < deadline:
                if process.poll() is not None:
                    break
                try:
                    line = out_queue.get(timeout=0.2)
                except queue.Empty:
                    continue

                stripped = line.rstrip('\n')
                startup_log.append(stripped)
                discovered = cls._extract_base_url(stripped)
                if discovered:
                    base_url = discovered
                    break

            if base_url is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

                log_tail = '\n'.join(startup_log[-20:])
                raise RuntimeError(
                    'Failed to start local EpiSuite server and detect startup URL within '
                    f'{timeout_seconds}s. Last log lines:\n{log_tail}'
                )

            cls._process = process
            cls._base_url = base_url
            cls._startup_log = startup_log[-200:]

            if not cls._atexit_registered:
                atexit.register(cls.stop)
                cls._atexit_registered = True

            return cls._base_url

    @classmethod
    def stop(cls):
        with cls._lock:
            if cls._process is None:
                return
            if cls._process.poll() is None:
                cls._process.terminate()
                try:
                    cls._process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    cls._process.kill()
            cls._process = None
            cls._base_url = None


def stop_local_episuite_server():
    """Stop the managed local EpiSuite runtime if it is running."""
    _LocalRuntimeManager.stop()

class EpiSuiteAPIClient:
    def __init__(self, base_url=None, api_key=None):
        mode = os.getenv('PYEPISUITE_MODE', 'auto').strip().lower()
        if mode not in {'auto', 'local', 'remote'}:
            raise ValueError("PYEPISUITE_MODE must be one of: auto, local, remote")

        resolved_base_url = base_url
        self.local_mode = False

        if resolved_base_url is None:
            explicit_local_base = os.getenv('PYEPISUITE_LOCAL_BASE_URL')

            if mode == 'remote':
                resolved_base_url = DEFAULT_REMOTE_BASE_URL
            elif explicit_local_base:
                resolved_base_url = _with_api_suffix(explicit_local_base)
                self.local_mode = True
            elif mode == 'local' or _LocalRuntimeManager.has_local_assets():
                resolved_base_url = _with_api_suffix(_LocalRuntimeManager.ensure_started())
                self.local_mode = True
            else:
                resolved_base_url = DEFAULT_REMOTE_BASE_URL
        elif re.match(r'^https?://(127\.0\.0\.1|localhost)(:\d+)?(/.*)?$', resolved_base_url):
            self.local_mode = True

        self.base_url = resolved_base_url
        self.api_key = api_key

    def _headers(self):
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def _parse_json_response(self, response, operation_name):
        response.raise_for_status()
        content_type = response.headers.get('content-type', '').lower()
        if 'application/json' not in content_type:
            snippet = response.text[:600].strip()
            raise ValueError(
                f'{operation_name} expected JSON but received {content_type or "unknown content type"}. '
                f'Response snippet: {snippet}'
            )
        return response.json()

    def search(self, query_term, time_out=10):
        """
        Search the EPISuite API with a query term (SMILES, CAS, or chemical name).

        Parameters:
            query_term (str): The term to search for.
            time_out (int): The time out for the request.

        Returns:
            List[Chemical]: A list of Chemical instances.
        """
        url = f'{self.base_url}/search'
        params = {'query': query_term}
        response = requests.get(url, params=params, headers=self._headers(), timeout=time_out)
        data = self._parse_json_response(response, 'search')

        # Convert each dictionary in the response to a Chemical instance
        ids = [Identifiers(**item) for item in data]
        return ids
    
    def submit(self, cas="", smiles=""):
        """
        Submit a CAS number or SMILES string to the EPISuite API.

        Parameters:
            cas (str): The CAS number of the chemical.
            smiles (str): The SMILES string of the chemical.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If neither 'cas' nor 'smiles' is provided.
        """
        if not cas and not smiles:
            raise ValueError("Either 'cas' or 'smiles' must be provided.")

        url = f'{self.base_url}/submit'
        params = {}
        if cas:
            params['cas'] = cas
        else:
            params['smiles'] = smiles

        response = requests.get(url, params=params, headers=self._headers(), timeout=120)
        try:
            return self._parse_json_response(response, 'submit')
        except ValueError as exc:
            if cas and self.local_mode and _is_cas_formatted(cas):
                normalized = _normalize_cas_for_local(cas)
                if normalized != cas:
                    retry_params = dict(params)
                    retry_params['cas'] = normalized
                    retry_response = requests.get(url, params=retry_params, headers=self._headers(), timeout=120)
                    return self._parse_json_response(retry_response, 'submit')
            raise exc

    @staticmethod
    def stop_local_runtime():
        """Stop the managed local runtime launched by this package."""
        stop_local_episuite_server()


class LocalEpiSuiteAPIClient(EpiSuiteAPIClient):
    """Explicit local client that always targets the local EpiSuite runtime."""

    def __init__(self, base_url=None, api_key=None):
        resolved_base_url = base_url or os.getenv('PYEPISUITE_LOCAL_BASE_URL')
        if resolved_base_url is None:
            resolved_base_url = _with_api_suffix(_LocalRuntimeManager.ensure_started())
        else:
            resolved_base_url = _with_api_suffix(resolved_base_url)

        super().__init__(base_url=resolved_base_url, api_key=api_key)
        self.local_mode = True
    
def from_dict(data_class, data):
    if isinstance(data_class, type):
        if hasattr(data_class, '__dataclass_fields__'):
            fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
            return data_class(**{f: from_dict(fieldtypes[f], data[f]) for f in data})
    elif hasattr(data_class, '__origin__'):
        origin = data_class.__origin__
        if origin is list:
            return [from_dict(data_class.__args__[0], item) for item in data]
        elif origin is Optional:
            return from_dict(data_class.__args__[0], data) if data is not None else None
    return data
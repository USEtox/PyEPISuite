import os
from unittest.mock import MagicMock, patch

from pyepisuite.api_client import EpiSuiteAPIClient, LocalEpiSuiteAPIClient


def _json_response(payload):
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.headers = {'content-type': 'application/json'}
    response.json.return_value = payload
    response.text = ''
    return response


def _text_response(text):
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.headers = {'content-type': 'text/plain'}
    response.text = text
    return response


def test_mode_remote_uses_hosted_api():
    with patch.dict(os.environ, {'PYEPISUITE_MODE': 'remote'}):
        client = EpiSuiteAPIClient()

    assert client.base_url == 'https://episuite.dev/api'
    assert client.local_mode is False


def test_mode_local_starts_managed_runtime():
    with patch.dict(os.environ, {'PYEPISUITE_MODE': 'local'}):
        with patch('pyepisuite.api_client._LocalRuntimeManager.ensure_started', return_value='http://127.0.0.1:45511'):
            client = EpiSuiteAPIClient()

    assert client.base_url == 'http://127.0.0.1:45511/api'
    assert client.local_mode is True


def test_mode_auto_prefers_local_when_assets_exist():
    with patch.dict(os.environ, {'PYEPISUITE_MODE': 'auto'}):
        with patch('pyepisuite.api_client._LocalRuntimeManager.has_local_assets', return_value=True):
            with patch('pyepisuite.api_client._LocalRuntimeManager.ensure_started', return_value='http://127.0.0.1:45511'):
                client = EpiSuiteAPIClient()

    assert client.base_url == 'http://127.0.0.1:45511/api'
    assert client.local_mode is True


def test_submit_retries_with_zero_padded_cas_in_local_mode():
    client = EpiSuiteAPIClient(base_url='http://127.0.0.1:45511/api')

    first = _text_response('Error: CAS not found in the database: 50-00-0')
    second = _json_response({'ok': True})

    with patch('pyepisuite.api_client.requests.get', side_effect=[first, second]) as mocked_get:
        result = client.submit(cas='50-00-0')

    assert result == {'ok': True}
    assert mocked_get.call_count == 2

    first_call_params = mocked_get.call_args_list[0].kwargs['params']
    second_call_params = mocked_get.call_args_list[1].kwargs['params']

    assert first_call_params['cas'] == '50-00-0'
    assert second_call_params['cas'] == '000050-00-0'


def test_explicit_local_client_uses_runtime_manager():
    with patch('pyepisuite.api_client._LocalRuntimeManager.ensure_started', return_value='http://127.0.0.1:45511'):
        client = LocalEpiSuiteAPIClient()

    assert client.local_mode is True
    assert client.base_url == 'http://127.0.0.1:45511/api'


def _make_jar(path, version=None, main_class='EpiCli'):
    """Write a minimal jar whose manifest optionally declares a version."""
    import zipfile

    lines = ['Manifest-Version: 1.0', f'Main-Class: {main_class}']
    if version is not None:
        lines += ['Implementation-Title: EPI Suite', f'Implementation-Version: {version}']
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('META-INF/MANIFEST.MF', '\r\n'.join(lines) + '\r\n')
    return path


def test_read_jar_version_reads_manifest(tmp_path):
    from pyepisuite.api_client import read_jar_version

    assert read_jar_version(_make_jar(tmp_path / 'new.jar', '1.1.0')) == '1.1.0'
    # Legacy EpiSuiteCLI builds declare no Implementation-Version
    assert read_jar_version(_make_jar(tmp_path / 'old.jar', None,
                                      'com.srcinc.episuite.EpiSuite')) is None
    # A non-jar must not raise
    (tmp_path / 'junk.jar').write_bytes(b'not a zip')
    assert read_jar_version(tmp_path / 'junk.jar') is None


def test_jar_is_supported_rejects_legacy_and_older_builds(tmp_path):
    from pyepisuite.api_client import jar_is_supported

    assert jar_is_supported(_make_jar(tmp_path / 'a.jar', '1.1.0')) is True
    assert jar_is_supported(_make_jar(tmp_path / 'b.jar', '1.2.0')) is True
    assert jar_is_supported(_make_jar(tmp_path / 'c.jar', '1.0.9')) is False
    # No version at all -> the legacy jar, which has no --serve mode
    assert jar_is_supported(_make_jar(tmp_path / 'd.jar', None)) is False


def test_has_local_assets_ignores_unsupported_jar(tmp_path):
    """`auto` mode must fall back to remote rather than fail on a stale jar."""
    from pyepisuite.api_client import _LocalRuntimeManager

    legacy = _make_jar(tmp_path / 'EpiSuiteCLI.jar', None, 'com.srcinc.episuite.EpiSuite')
    with patch.dict(os.environ, {'PYEPISUITE_LOCAL_JAR_PATH': str(legacy)}):
        assert _LocalRuntimeManager.has_local_assets() is False

    current = _make_jar(tmp_path / 'current.jar', '1.1.0')
    with patch.dict(os.environ, {'PYEPISUITE_LOCAL_JAR_PATH': str(current)}):
        assert _LocalRuntimeManager.has_local_assets() is True


def test_acquire_jar_refuses_to_replace_an_explicitly_chosen_jar(tmp_path):
    import pytest
    from pyepisuite.api_client import _LocalRuntimeManager

    legacy = _make_jar(tmp_path / 'EpiSuiteCLI.jar', None, 'com.srcinc.episuite.EpiSuite')
    with patch.dict(os.environ, {'PYEPISUITE_LOCAL_JAR_PATH': str(legacy)}):
        with patch.object(_LocalRuntimeManager, '_download_jar') as download:
            with pytest.raises(RuntimeError, match='needs EPI Suite 1.1.0 or newer'):
                _LocalRuntimeManager._acquire_jar()
            download.assert_not_called()


def test_acquire_jar_replaces_a_discovered_stale_jar(tmp_path):
    from pyepisuite.api_client import _LocalRuntimeManager

    stale = _make_jar(tmp_path / 'EpiSuiteCLI.jar', None, 'com.srcinc.episuite.EpiSuite')
    fresh = _make_jar(tmp_path / 'downloaded.jar', '1.1.0')
    env = {k: v for k, v in os.environ.items() if k != 'PYEPISUITE_LOCAL_JAR_PATH'}
    with patch.dict(os.environ, env, clear=True):
        with patch.object(_LocalRuntimeManager, '_resolve_jar_path', return_value=stale):
            with patch.object(_LocalRuntimeManager, '_download_jar', return_value=fresh) as dl:
                assert _LocalRuntimeManager._acquire_jar() == fresh
                dl.assert_called_once()


def test_acquire_jar_raises_when_the_download_is_also_unsupported(tmp_path):
    import pytest
    from pyepisuite.api_client import _LocalRuntimeManager

    stale = _make_jar(tmp_path / 'EpiSuiteCLI.jar', '1.0.0')
    env = {k: v for k, v in os.environ.items() if k != 'PYEPISUITE_LOCAL_JAR_PATH'}
    with patch.dict(os.environ, env, clear=True):
        with patch.object(_LocalRuntimeManager, '_resolve_jar_path', return_value=stale):
            with patch.object(_LocalRuntimeManager, '_download_jar', return_value=stale):
                with pytest.raises(RuntimeError, match='PYEPISUITE_MODE=remote'):
                    _LocalRuntimeManager._acquire_jar()


def test_extract_base_url_matches_the_runtime_log_line():
    """Guards the startup regex against the jar's actual output."""
    from pyepisuite.api_client import _LocalRuntimeManager

    line = '2026-09-08 15:46:01.473 | INFO | Listening at http://127.0.0.1:44967/ |  |  |'
    assert _LocalRuntimeManager._extract_base_url(line) == 'http://127.0.0.1:44967'
    assert _LocalRuntimeManager._extract_base_url('nothing to see here') is None

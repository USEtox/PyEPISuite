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

    assert client.base_url == 'https://episuite.dev/EpiWebSuite/api'
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

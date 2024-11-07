# tests/test_api_client.py

import pytest
from pyepisuite.api_client import EpiSuiteAPIClient
from pyepisuite.models import Identifiers

@pytest.fixture
def client():
    return EpiSuiteAPIClient()

@pytest.mark.network
def test_search(client):
    identifiers = client.search('formaldehyde')
    assert isinstance(identifiers, list), "Identifiers should be a list."
    assert len(identifiers) > 0, "Identifiers list should not be empty."
    assert isinstance(identifiers[0], Identifiers), "First item should be an instance of Identifiers."
    assert identifiers[0].name == 'FORMALDEHYDE', "First identifier name should be 'FORMALDEHYDE'."
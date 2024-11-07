# tests/test_utils.py

import pytest
from unittest.mock import patch, MagicMock
from pyepisuite.api_client import EpiSuiteAPIClient
from pyepisuite.models import Identifiers
from pyepisuite.utils import is_valid_cas, search_episuite_by_cas

@pytest.mark.parametrize("cas", [
    "50-00-0",       # Formaldehyde
    "7732-18-5",     # Water
    "64-17-5",       # Ethanol
    "67-56-1",       # Methanol
    "0000000-00-0"   # Hypothetical valid CAS
])
def test_valid_cas_numbers(cas):
    """Test that valid CAS numbers are correctly identified."""
    assert is_valid_cas(cas), f"CAS Number '{cas}' should be valid."

@pytest.mark.parametrize("cas", [
    "123-45-6",
    "67-56-2"         # Modified to have an incorrect check digit
])
def test_invalid_check_digits(cas):
    """Test that CAS numbers with incorrect check digits are invalid."""
    assert not is_valid_cas(cas), f"CAS Number '{cas}' should have an invalid check digit."

@pytest.mark.parametrize("cas", [
    "12-345-6",        # Incorrect grouping
    "invalid-cas-123", # Non-digit characters
    "123-456-789",     # Excessive digits
    "1234567-89-0a",   # Extra characters
    "12-34-56-7",      # Extra parts
    "1234567890"       # No hyphens
])
def test_invalid_formats(cas):
    """Test that CAS numbers with incorrect formats are invalid."""
    assert not is_valid_cas(cas), f"CAS Number '{cas}' should have an invalid format."

@pytest.mark.parametrize("cas, expected", [
    ("1234567-89-0", False), # Depends on check digit
    ("0000000-00-0", True),  # Hypothetical valid CAS
    ("", False),              # Empty string
    ("123-45", False),        # Missing parts
    ("1234567890", False),    # No hyphens
    ("12-34-56-7", False)     # Extra parts
])
def test_edge_cases(cas, expected):
    """Test edge cases for CAS numbers."""
    assert is_valid_cas(cas) == expected, f"CAS Number '{cas}' validity should be {expected}."

def test_none_input():
    """Test that passing None as input returns False."""
    assert not is_valid_cas(None), "Passing None should return False."

@pytest.mark.parametrize("input_value", [
    1234567890,          # Integer
    64.17,               # Float
    ["64-17-5"],         # List
    {"cas": "64-17-5"},  # Dictionary
    True,                # Boolean
    None                 # NoneType
])
def test_non_string_input(input_value):
    """Test that passing non-string types returns False."""
    assert not is_valid_cas(input_value), f"Non-string input '{input_value}' should return False."


# API calls from utils functions =============================================
@pytest.fixture
def client():
    """Fixture to initialize and provide an instance of EpiSuiteAPIClient."""
    return EpiSuiteAPIClient()

def test_search_single_valid_cas(client):
    """Test search_episuite_by_cas with a single valid CAS number."""
    cas_numbers = ["50-00-0"]  # Formaldehyde
    result = search_episuite_by_cas(cas_numbers)
    assert isinstance(result, list), "Result should be a list."
    assert len(result) == 1, "Result list should contain one identifier."
    identifier = result[0]
    assert isinstance(identifier, Identifiers), "Identifier should be an instance of Identifiers."
    assert identifier.name == "FORMALDEHYDE", "Identifier name should be 'FORMALDEHYDE'."

def test_search_multiple_valid_cas(client):
    """Test search_episuite_by_cas with multiple valid CAS numbers."""
    cas_numbers = ["50-00-0", "64-17-5"]  # Formaldehyde and Ethanol
    result = search_episuite_by_cas(cas_numbers)
    assert isinstance(result, list), "Result should be a list."
    assert len(result) == 2, "Result list should contain two identifiers."
    identifier1, identifier2 = result
    assert isinstance(identifier1, Identifiers), "First identifier should be an instance of Identifiers."
    assert identifier1.name == "FORMALDEHYDE", "First identifier name should be 'FORMALDEHYDE'."
    assert isinstance(identifier2, Identifiers), "Second identifier should be an instance of Identifiers."
    assert identifier2.name == "ETHANOL", "Second identifier name should be 'ETHANOL'."

def test_search_invalid_cas(client):
    """Test search_episuite_by_cas with invalid CAS numbers."""
    cas_numbers = ["123-45-6"]  # Invalid CAS
    result = search_episuite_by_cas(cas_numbers)
    assert isinstance(result, list), "Result should be a list."
    assert len(result) == 0, "Result list should be empty for invalid CAS."

def test_search_empty_list(client):
    """Test search_episuite_by_cas with an empty list of CAS numbers."""
    cas_numbers = []
    result = search_episuite_by_cas(cas_numbers)
    assert isinstance(result, list), "Result should be a list."
    assert len(result) == 0, "Result should be empty for empty input."

def test_search_none_input(client):
    """Test search_episuite_by_cas with None as input."""
    with pytest.raises(TypeError):
        search_episuite_by_cas(None)
import dacite
from .models import ResultEcoSAR, ResultEPISuite, Identifiers
from .api_client import EpiSuiteAPIClient
from typing import List, Any
import re
import logging

def json_to_episuite(json_data):
    """
    Convert a JSON response from the EPISuite API to a Chemical instance.

    Parameters:
        json_data (dict): The JSON response from the API.

    Returns:
        ResultEPISuite: A ResultEPISuite instance.
    """
    return dacite.from_dict(data_class=ResultEPISuite, data=json_data)

def json_to_ecosar(json_data):
    """
    Convert a JSON response from the EcoSAR API to a Chemical instance.

    Parameters:
        json_data (dict): The JSON response from the API (submit). For the response of submit method,
        the key is "ecosar". 

    Returns:
        ResultEcoSAR: A ResultEcoSAR instance.
    """
    return dacite.from_dict(data_class=ResultEcoSAR, data=json_data)

def search_episuite_by_cas(query_term: List[str]) -> List[Identifiers]:
    """
    Search the EPISuite API with a query term (SMILES, CAS, or chemical name).

    Parameters:
        query_term (str): The term to search for.

    Returns:
        List[Identifiers]: A list of Identifiers instances.
    """
    client = EpiSuiteAPIClient()
    identifiers = []
    for term in query_term:
        # check if term is a CAS number
        if is_valid_cas(term):
            identifiers += client.search(term)
        else:
            logging.warning(f"Query term '{term}' is not a valid CAS number.")
    return identifiers

def search_episuite(query_terms: List[str]) -> List[Identifiers]:
    """
    Search the EPISuite API with a query term (SMILES, CAS, or chemical name).

    Parameters:
        query_term (str): The term to search for.

    Returns:
        List[Identifiers]: A list of Identifiers instances.
    """
    client = EpiSuiteAPIClient()
    identifiers = []
    for term in query_terms:
        identifiers += client.search(term)
    return identifiers

def submit_to_episuite(identifiers: List[Identifiers]) -> tuple[List[ResultEPISuite], List[ResultEcoSAR]]:
    """
    Submit an identifier to the EPISuite API.

    Parameters:
        identifiers: List of identifiers; the identifiers obtained by calling search_episuite_by_cas. 
        It can be a list of CAS numbers or SMILES strings. Note that the CAS numbers are preferred, 
        and they must be in the correct format, i.e. with leading zeros and hyphens.

    Returns:
        List[ResultEPISuite, ResultEcoSAR]: A list of ResultEPISuite and ResultEcoSAR instances.
    """
    client = EpiSuiteAPIClient()
    epi_results = []
    ecosar_results = []
    for id in identifiers:
        if id.cas:
            res = client.submit(cas=id.cas)
            epi_results.append(json_to_episuite(res))
            ecosar_results.append(json_to_ecosar(res['ecosar']))
        elif id.smiles:
            res = client.submit(smiles=id.smiles)
            epi_results.append(json_to_episuite(res))
            ecosar_results.append(json_to_ecosar(res['ecosar']))
        else:
            logging.warning(f"Identifier '{id.name}' does not contain a CAS number or SMILES string.")
    return epi_results, ecosar_results

def is_valid_cas(cas: Any) -> bool:
    """
    Validate a CAS (Chemical Abstracts Service) number.

    Parameters:
        cas (Any): The CAS number to validate.

    Returns:
        bool: True if the CAS number is valid, False otherwise.
    """
    # Ensure the input is a string
    if not isinstance(cas, str):
        print(f"Invalid input type: Expected string, got {type(cas).__name__}.")
        return False

    # Regular expression to match the CAS format: XX-XX-XX, XXX-XX-X, etc.
    cas_pattern = re.compile(r'^(\d{2,7})-(\d{2})-(\d)$')
    match = cas_pattern.match(cas)

    if not match:
        print(f"CAS number '{cas}' does not match the required format.")
        return False

    # Extract all digits as a single string
    digits = ''.join(match.groups())

    # The last digit is the check digit
    try:
        check_digit = int(digits[-1])
    except (IndexError, ValueError):
        print(f"CAS number '{cas}' is missing a check digit or contains non-digit characters.")
        return False

    # The digits to be used for calculating the check digit (exclude the last digit)
    digits_to_check = digits[:-1]

    # Reverse the digits for weighting
    reversed_digits = digits_to_check[::-1]

    # Calculate the weighted sum
    total = 0
    for idx, digit_char in enumerate(reversed_digits, start=1):
        try:
            digit = int(digit_char)
        except ValueError:
            print(f"CAS number '{cas}' contains non-digit characters.")
            return False
        total += digit * idx

    # Calculate the expected check digit
    expected_check_digit = total % 10

    if check_digit == expected_check_digit:
        return True
    else:
        print(f"CAS number '{cas}' has an invalid check digit. Expected {expected_check_digit}, got {check_digit}.")
        return False
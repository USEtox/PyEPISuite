import dacite
from dacite import Config
from .models import ResultEcoSAR, ResultEPISuite, Identifiers, ensure_flags
from .api_client import EpiSuiteAPIClient
from typing import Dict, List, Any
import re
import logging
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

def _flags_hook(v: Any) -> Dict[str, bool] | None:
    return ensure_flags(v)

def get_dacite_config() -> Config:
    # Hook Dict[str, bool] so any field annotated as that will be normalized during from_dict
    return Config(type_hooks={Dict[str, bool]: _flags_hook})

def get_cache_dir() -> Path:
    """Get or create the cache directory."""
    cache_dir = Path.home() / ".pyepisuite_cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def get_search_cache_key(query_terms: List[str], search_type: str = "general") -> str:
    """Generate a unique cache key for search queries."""
    # Sort terms for consistent cache keys regardless of order
    sorted_terms = sorted(query_terms)
    key_data = f"search_{search_type}:{','.join(sorted_terms)}"
    return hashlib.md5(key_data.encode()).hexdigest()

def save_search_to_cache(cache_key: str, identifiers: List[Identifiers]):
    """Save search results to cache."""
    try:
        cache_dir = get_cache_dir()
        cache_file = cache_dir / f"search_{cache_key}.json"
        
        # Convert identifiers to dict for JSON serialization
        cache_data = {
            "identifiers": [asdict(identifier) for identifier in identifiers],
            "cached_at": datetime.now().isoformat(),
            "count": len(identifiers)
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
            
        logging.debug(f"Cached search results for key: {cache_key}")
        
    except Exception as e:
        logging.warning(f"Failed to save search results to cache: {e}")

def load_search_from_cache(cache_key: str) -> List[Identifiers] | None:
    """Load search results from cache if available."""
    try:
        cache_dir = get_cache_dir()
        cache_file = cache_dir / f"search_{cache_key}.json"
        
        if not cache_file.exists():
            return None
            
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            
        # Convert dict back to Identifiers instances
        identifiers = []
        for identifier_data in cache_data["identifiers"]:
            identifier = dacite.from_dict(
                data_class=Identifiers,
                data=identifier_data,
                config=get_dacite_config()
            )
            identifiers.append(identifier)
        
        logging.debug(f"Loaded search results from cache: {cache_key} ({len(identifiers)} identifiers)")
        return identifiers
        
    except Exception as e:
        logging.warning(f"Failed to load search results from cache: {e}")
        return None

def get_cache_key(identifier: Identifiers) -> str:
    """Generate a unique cache key for an identifier."""
    if identifier.cas:
        key_data = f"cas:{identifier.cas}"
    elif identifier.smiles:
        key_data = f"smiles:{identifier.smiles}"
    else:
        key_data = f"name:{identifier.name}"
    
    # Create hash for filename safety
    return hashlib.md5(key_data.encode()).hexdigest()

def save_to_cache(cache_key: str, epi_result: ResultEPISuite, ecosar_result: ResultEcoSAR):
    """Save results to cache."""
    try:
        cache_dir = get_cache_dir()
        cache_file = cache_dir / f"{cache_key}.json"
        
        # Convert dataclass instances to dict for JSON serialization
        cache_data = {
            "epi_result": asdict(epi_result),
            "ecosar_result": asdict(ecosar_result),
            "cached_at": datetime.now().isoformat()
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
            
        logging.debug(f"Cached results for key: {cache_key}")
        
    except Exception as e:
        logging.warning(f"Failed to save to cache: {e}")

def load_from_cache(cache_key: str) -> tuple[ResultEPISuite, ResultEcoSAR] | None:
    """Load results from cache if available."""
    try:
        cache_dir = get_cache_dir()
        cache_file = cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
            
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            
        # Convert dict back to dataclass instances
        epi_result = dacite.from_dict(
            data_class=ResultEPISuite, 
            data=cache_data["epi_result"], 
            config=get_dacite_config()
        )
        ecosar_result = dacite.from_dict(
            data_class=ResultEcoSAR, 
            data=cache_data["ecosar_result"], 
            config=get_dacite_config()
        )
        
        logging.debug(f"Loaded from cache: {cache_key}")
        return epi_result, ecosar_result
        
    except Exception as e:
        logging.warning(f"Failed to load from cache: {e}")
        return None

def clear_cache():
    """Clear all cached results."""
    try:
        cache_dir = get_cache_dir()
        for cache_file in cache_dir.glob("*.json"):
            cache_file.unlink()
        logging.info("Cache cleared successfully")
    except Exception as e:
        logging.warning(f"Failed to clear cache: {e}")

def json_to_episuite(json_data):
    """
    Convert a JSON response from the EPISuite API to a Chemical instance.

    Parameters:
        json_data (dict): The JSON response from the API.

    Returns:
        ResultEPISuite: A ResultEPISuite instance.
    """
    return dacite.from_dict(data_class=ResultEPISuite, data=json_data, config=get_dacite_config())

def json_to_ecosar(json_data):
    """
    Convert a JSON response from the EcoSAR API to a Chemical instance.

    Parameters:
        json_data (dict): The JSON response from the API (submit). For the response of submit method,
        the key is "ecosar". 

    Returns:
        ResultEcoSAR: A ResultEcoSAR instance.
    """
    return dacite.from_dict(data_class=ResultEcoSAR, data=json_data, config=get_dacite_config())

def search_episuite_by_cas(CASRN: List[str], use_cache: bool = True) -> List[Identifiers]:
    """
    Search the EPISuite API with a CAS number.

    Parameters:
        CASRN (List[str]): The CAS numbers to search for.
        use_cache (bool): Whether to use caching for the search results. Defaults to True.

    Returns:
        List[Identifiers]: A list of Identifiers instances.
    """
    # Check cache first if enabled
    if use_cache:
        cache_key = get_search_cache_key(CASRN)
        cached_result = load_search_from_cache(cache_key)
        if cached_result is not None:
            logging.info(f"Search results for CAS numbers {CASRN} loaded from cache")
            return cached_result
    
    client = EpiSuiteAPIClient()
    identifiers = []
    for term in CASRN:
        # check if term is a CAS number
        if is_valid_cas(term):
            identifiers += client.search(term)
        else:
            logging.warning(f"Query term '{term}' is not a valid CAS number.")
    
    # Save to cache if enabled
    if use_cache and identifiers:
        save_search_to_cache(cache_key, identifiers)
        logging.info(f"Search results for CAS numbers {CASRN} saved to cache")
    
    return identifiers

def search_episuite(query_terms: List[str], use_cache: bool = True) -> List[Identifiers]:
    """
    Search the EPISuite API with a query term (SMILES, CAS, or chemical name).

    Parameters:
        query_terms (List[str]): The terms to search for.
        use_cache (bool): Whether to use caching for the search results. Defaults to True.

    Returns:
        List[Identifiers]: A list of Identifiers instances.
    """
    # Check cache first if enabled
    if use_cache:
        cache_key = get_search_cache_key(query_terms)
        cached_result = load_search_from_cache(cache_key)
        if cached_result is not None:
            logging.info(f"Search results for query terms {query_terms} loaded from cache")
            return cached_result
    
    client = EpiSuiteAPIClient()
    identifiers = []
    for term in query_terms:
        identifiers += client.search(term)
    
    # Save to cache if enabled
    if use_cache and identifiers:
        save_search_to_cache(cache_key, identifiers)
        logging.info(f"Search results for query terms {query_terms} saved to cache")
    
    return identifiers

def submit_to_episuite(identifiers: List[Identifiers], use_cache: bool = True) -> tuple[List[ResultEPISuite], List[ResultEcoSAR]]:
    """
    Submit an identifier to the EPISuite API with caching support.

    Parameters:
        identifiers: List of identifiers; the identifiers obtained by calling search_episuite_by_cas. 
        It can be a list of CAS numbers or SMILES strings. Note that the CAS numbers are preferred, 
        and they must be in the correct format, i.e. with leading zeros and hyphens.
        use_cache (bool): Whether to use caching. Default is True.

    Returns:
        List[ResultEPISuite, ResultEcoSAR]: A list of ResultEPISuite and ResultEcoSAR instances.
    """
    client = EpiSuiteAPIClient()
    epi_results = []
    ecosar_results = []
    
    for id in identifiers:
        cache_key = get_cache_key(id) if use_cache else None
        
        # Try to load from cache first
        if use_cache and cache_key:
            cached_results = load_from_cache(cache_key)
            if cached_results:
                epi_result, ecosar_result = cached_results
                epi_results.append(epi_result)
                ecosar_results.append(ecosar_result)
                logging.info(f"Using cached results for {id.cas or id.smiles or id.name}")
                continue
        
        # Make API call if not in cache
        try:
            if id.cas:
                res = client.submit(cas=id.cas)
                epi_result = json_to_episuite(res)
                ecosar_result = json_to_ecosar(res['ecosar'])
                
                # Save to cache
                if use_cache and cache_key:
                    save_to_cache(cache_key, epi_result, ecosar_result)
                    
                epi_results.append(epi_result)
                ecosar_results.append(ecosar_result)
                logging.info(f"API call completed for {id.cas}")
                
            elif id.smiles:
                res = client.submit(smiles=id.smiles)
                epi_result = json_to_episuite(res)
                ecosar_result = json_to_ecosar(res['ecosar'])
                
                # Save to cache
                if use_cache and cache_key:
                    save_to_cache(cache_key, epi_result, ecosar_result)
                    
                epi_results.append(epi_result)
                ecosar_results.append(ecosar_result)
                logging.info(f"API call completed for {id.smiles}")
                
            else:
                logging.warning(f"Identifier '{id.name}' does not contain a CAS number or SMILES string.")
                
        except Exception as e:
            logging.error(f"Failed to process identifier {id.cas or id.smiles or id.name}: {e}")
            
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
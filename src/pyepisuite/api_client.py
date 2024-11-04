import requests
from .models import ResultEPISuite, Identifiers
from typing import Optional

class EpiSuiteAPIClient:
    def __init__(self, base_url='https://episuite.dev/EpiWebSuite/api', api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    def search(self, query_term):
        """
        Search the EPISuite API with a query term (SMILES, CAS, or chemical name).

        Parameters:
            query_term (str): The term to search for.

        Returns:
            List[Chemical]: A list of Chemical instances.
        """
        url = f'{self.base_url}/search'
        params = {'query': query_term}
        headers = {}

        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Convert each dictionary in the response to a Chemical instance
        chemicals = [Identifiers(**item) for item in data]
        return chemicals
    
    def submit(self, cas=None, smiles=None):
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

        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        # remove output from the response
        data.pop('output', None)
        return data
    
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
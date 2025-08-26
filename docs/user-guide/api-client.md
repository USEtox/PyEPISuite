# API Client

The `EpiSuiteAPIClient` class provides the core interface for interacting with the EPISuite API.

## Overview

::: pyepisuite.api_client.EpiSuiteAPIClient
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: true

## Usage Examples

### Basic Client Setup

```python
from pyepisuite import EpiSuiteAPIClient

# Create client with default settings
client = EpiSuiteAPIClient()

# Or with custom base URL
client = EpiSuiteAPIClient(base_url='https://episuite.dev/EpiWebSuite/api')

# With API key (if required)
client = EpiSuiteAPIClient(api_key='your-api-key')
```

### Searching for Chemicals

```python
# Search by CAS number
results = client.search('50-00-0')

# Search by SMILES
results = client.search('C=O')

# Search by chemical name
results = client.search('formaldehyde')
```

### Submitting for Predictions

```python
# Submit using CAS number
predictions = client.submit(cas='50-00-0')

# Submit using SMILES
predictions = client.submit(smiles='C=O')

# The response includes both EPI Suite and EcoSAR results
print(predictions.keys())  # ['chemicalProperties', 'logKow', ..., 'ecosar']
```

## Error Handling

The API client includes robust error handling:

```python
import requests

try:
    results = client.search('invalid-identifier')
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Invalid parameters: {e}")
```

## Configuration Options

### Timeout Settings

```python
# Custom timeout for slow networks
results = client.search('50-00-0', time_out=30)
```

### API Key Authentication

If the API requires authentication:

```python
client = EpiSuiteAPIClient(api_key='your-api-key-here')
```

## Related Functions

For higher-level operations, see the utility functions:

- [`search_episuite_by_cas()`](../api-reference/utils.md#pyepisuite.utils.search_episuite_by_cas)
- [`search_episuite()`](../api-reference/utils.md#pyepisuite.utils.search_episuite)  
- [`submit_to_episuite()`](../api-reference/utils.md#pyepisuite.utils.submit_to_episuite)

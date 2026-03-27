# API Client

The `EpiSuiteAPIClient` class provides the core interface for interacting with the EPISuite API.

By default, the client now prefers a local runtime when `data/local/EpiSuiteCLI.jar` is available.
Set `PYEPISUITE_MODE=remote` to force the hosted API.

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

# Create client with default settings.
# If a local JAR is present, this starts local mode automatically.
client = EpiSuiteAPIClient()

# Or with custom base URL
client = EpiSuiteAPIClient(base_url='https://episuite.dev/EpiWebSuite/api')

# With API key (if required)
client = EpiSuiteAPIClient(api_key='your-api-key')
```

### Explicit Local Client

```python
from pyepisuite import LocalEpiSuiteAPIClient, stop_local_episuite_server

# Always target local runtime.
client = LocalEpiSuiteAPIClient()

ids = client.search('formaldehyde')
result = client.submit(cas='000050-00-0')

# Stop managed local process when needed.
stop_local_episuite_server()
```

### Mode Selection

Use `PYEPISUITE_MODE` to control behavior:

- `auto` (default): prefer local runtime if JAR exists, otherwise use remote API
- `local`: require local runtime and fail fast if startup fails
- `remote`: always use hosted API

Optional local environment variables:

- `PYEPISUITE_LOCAL_JAR_PATH`: absolute/relative path to `EpiSuiteCLI.jar`
- `PYEPISUITE_LOCAL_BASE_URL`: connect-only mode, e.g. `http://127.0.0.1:45511`
- `PYEPISUITE_LOCAL_STARTUP_TIMEOUT`: startup timeout in seconds (default `60`)

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

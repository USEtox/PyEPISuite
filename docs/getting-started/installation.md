# Installation

## Requirements

PyEPISuite requires Python 3.7 or higher and the following dependencies:

- `requests` - For API communication
- `dacite` - For data class conversion
- `pandas` - For DataFrame functionality
- `openpyxl` - For Excel export support

## Installation Methods

### Using pip (Recommended)

Install PyEPISuite directly from PyPI:

```bash
pip install pyepisuite
```

### From Source

For development or to get the latest features:

```bash
git clone https://github.com/USEtox/PyEPISuite.git
cd PyEPISuite
pip install -e .
```

### Using conda

If you prefer conda:

```bash
conda install -c conda-forge pyepisuite
```

## Verify Installation

Test your installation by running:

```python
import pyepisuite
print(f"PyEPISuite version: {pyepisuite.__version__}")

# Test basic functionality
from pyepisuite import EpiSuiteAPIClient
client = EpiSuiteAPIClient()
print("✅ Installation successful!")
```

## Optional Dependencies

For enhanced functionality, consider installing these optional packages:

### For Data Visualization
```bash
pip install matplotlib seaborn plotly
```

### For Jupyter Notebooks
```bash
pip install jupyter ipywidgets
```

### For Development
```bash
pip install pytest black isort mypy
```

## Troubleshooting

### Common Issues

#### ImportError: No module named 'pyepisuite'

Make sure you've installed the package correctly:
```bash
pip install --upgrade pyepisuite
```

#### SSL Certificate Issues

If you encounter SSL errors when accessing the API:
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

#### Firewall/Proxy Issues

If you're behind a corporate firewall, you may need to configure proxy settings:
```python
import requests
proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}
# Pass proxies to requests calls if needed
```

### Getting Help

If you continue to have issues:

1. Check the [GitHub Issues](https://github.com/USEtox/PyEPISuite/issues) page
2. Create a new issue with your system information and error messages
3. Join the [GitHub Discussions](https://github.com/USEtox/PyEPISuite/discussions) for community support

## Next Steps

Now that you have PyEPISuite installed, head over to the [Quick Start Guide](quickstart.md) to learn the basics!

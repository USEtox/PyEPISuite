# PyEPISuite Documentation

Welcome to **PyEPISuite**, a comprehensive Python client for the EPISuite API with advanced DataFrame utilities for environmental chemistry and toxicology research.

## Overview

PyEPISuite provides a simple, yet powerful interface to access EPA's EPISuite model predictions for environmental fate and transport properties, bioconcentration factors, and ecotoxicity estimates. The package includes convenient utilities to convert results into pandas DataFrames for easy data analysis and visualization.

## Key Features

### 🔗 **API Integration**
- Simple interface to EPISuite and EcoSAR APIs
- Search chemicals by CAS number, SMILES, or name
- Retrieve comprehensive environmental fate predictions

### 📊 **DataFrame Support**
- Convert API results to pandas DataFrames
- Combine EPI Suite and EcoSAR data
- Extract experimental values for validation
- Export to Excel with multiple sheets

### 🧪 **Experimental Data**
- Access curated experimental datasets
- Henry's law constants, solubility, and more
- Data validation and quality control

### 📈 **Analysis Ready**
- Summary statistics generation
- Data visualization support
- Batch processing capabilities

## Quick Example

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import episuite_to_dataframe, ecosar_to_dataframe

# Search for chemicals
cas_list = ["50-00-0", "100-00-5", "100-02-7"]
ids = search_episuite_by_cas(cas_list)

# Get predictions
epi_results, ecosar_results = submit_to_episuite(ids)

# Convert to DataFrames
epi_df = episuite_to_dataframe(epi_results)
ecosar_df = ecosar_to_dataframe(ecosar_results)

print(f"Retrieved data for {len(epi_df)} chemicals")
print(f"Available properties: {len(epi_df.columns)} columns")
```

## What's New in Version 0.1.0

- ✨ **DataFrame utilities** for easy data manipulation
- 📊 **Excel export** functionality  
- 🧮 **Summary statistics** generation
- 📚 **Comprehensive documentation** with examples
- 🧪 **Experimental data access** for validation

## Getting Started

Ready to dive in? Check out our [Installation Guide](getting-started/installation.md) and [Quick Start Tutorial](getting-started/quickstart.md).

## Support

- 📖 **Documentation**: Comprehensive guides and API reference
- 💡 **Examples**: Real-world usage scenarios
- 🐛 **Issues**: Report bugs on [GitHub](https://github.com/USEtox/PyEPISuite/issues)
- 💬 **Discussions**: Ask questions in [GitHub Discussions](https://github.com/USEtox/PyEPISuite/discussions)

## Contributing

We welcome contributions! See our [Contributing Guide](contributing.md) for details on how to get involved.

## License

PyEPISuite is licensed under the MIT License. See the [LICENSE](https://github.com/USEtox/PyEPISuite/blob/main/LICENSE) file for details.

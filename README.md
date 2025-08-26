# PyEPISuite

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-green.svg)](https://your-username.github.io/PyEPISuite/)
[![CI Tests](https://github.com/your-username/PyEPISuite/workflows/Tests/badge.svg)](https://github.com/your-username/PyEPISuite/actions)
[![Code Quality](https://github.com/your-username/PyEPISuite/workflows/Code%20Quality/badge.svg)](https://github.com/your-username/PyEPISuite/actions)

A comprehensive Python client for the EPISuite API with advanced DataFrame utilities for environmental chemistry and toxicology research.

## 🚀 Key Features

- **🔗 Complete API Integration**: Access EPA's EPISuite and EcoSAR models
- **📊 DataFrame Support**: Convert results to pandas DataFrames for analysis  
- **📈 Data Analysis Tools**: Built-in statistical and visualization utilities
- **🧪 Experimental Data**: Access curated experimental datasets for validation
- **📑 Excel Export**: Multi-sheet export with customizable formatting
- **📚 Comprehensive Documentation**: Detailed guides and examples

## 🛠️ Installation

### Using pip (Recommended)
```bash
pip install pyepisuite
```

### From Source
```bash
git clone https://github.com/USEtox/PyEPISuite.git
cd PyEPISuite
pip install -e .
```

## 📖 Quick Start

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import episuite_to_dataframe, ecosar_to_dataframe

# Search for chemicals
cas_list = ["50-00-0", "100-00-5", "100-02-7"]  
ids = search_episuite_by_cas(cas_list)

# Get predictions
epi_results, ecosar_results = submit_to_episuite(ids)

# Convert to DataFrames for analysis
epi_df = episuite_to_dataframe(epi_results)
ecosar_df = ecosar_to_dataframe(ecosar_results)

print(f"Retrieved data for {len(epi_df)} chemicals")
print(f"Properties available: {list(epi_df.columns)}")
```

## 🧮 DataFrame Features

PyEPISuite provides powerful DataFrame utilities for data analysis:

```python
from pyepisuite.dataframe_utils import (
    episuite_to_dataframe,
    ecosar_to_dataframe, 
    combine_episuite_ecosar_dataframes,
    export_to_excel,
    create_summary_statistics
)

# Convert API results to structured DataFrames
epi_df = episuite_to_dataframe(epi_results)          # 41 EPI Suite properties
ecosar_df = ecosar_to_dataframe(ecosar_results)      # 12 EcoSAR columns

# Combine datasets
combined_df = combine_episuite_ecosar_dataframes(epi_df, ecosar_df)

# Generate summary statistics
stats = create_summary_statistics(epi_df)

# Export to Excel with multiple sheets
export_to_excel({
    'EPI_Suite': epi_df,
    'EcoSAR': ecosar_df,
    'Statistics': stats
}, 'analysis_results.xlsx')
```

## 🧪 Experimental Data Integration

Access curated experimental datasets for model validation:

```python
from pyepisuite.expdata import HenryData, SolubilityData

# Load experimental data
henry_data = HenryData()
solubility_data = SolubilityData()

# Get experimental values
cas = "50-00-0"
experimental_hlc = henry_data.HLC(cas)
experimental_solubility = solubility_data.solubility(cas)

# Compare with predictions
predicted_hlc = epi_df[epi_df['cas'] == cas]['henrys_law_constant_estimated'].iloc[0]
print(f"Predicted: {predicted_hlc}, Experimental: {experimental_hlc}")
```

## 📊 Available Properties

PyEPISuite provides access to 40+ environmental and physical-chemical properties:

### Physical Properties
- Log Kow, Melting Point, Boiling Point
- Vapor Pressure, Water Solubility, Henry's Law Constant
- Log Koa, Log Koc

### Environmental Fate
- Atmospheric Half-life, Biodegradation Rates
- Aerosol Adsorption, Bioconcentration Factor
- Water Volatilization, Fugacity Model Results

### Ecotoxicity (via EcoSAR)
- Acute and chronic toxicity predictions
- Fish, Daphnid, and Algae endpoints
- Multiple QSAR model classes

## 📚 Documentation

- **[Installation Guide](https://pyepisuite.readthedocs.io/getting-started/installation/)**
- **[Quick Start Tutorial](https://pyepisuite.readthedocs.io/getting-started/quickstart/)**
- **[DataFrame Utilities Guide](https://pyepisuite.readthedocs.io/user-guide/dataframe-utils/)**
- **[Data Analysis Examples](https://pyepisuite.readthedocs.io/examples/data-analysis/)**
- **[API Reference](https://pyepisuite.readthedocs.io/api-reference/)**

## 🔬 Research Applications

PyEPISuite is ideal for:

- **Environmental Risk Assessment**: Screening chemicals for persistence, bioaccumulation, and toxicity
- **QSAR Model Development**: Large-scale property prediction and validation
- **Regulatory Compliance**: Generating data for chemical registration
- **Academic Research**: High-throughput environmental fate modeling
- **Chemical Prioritization**: Ranking chemicals by environmental concern

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Links
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Issue Templates](.github/ISSUE_TEMPLATE/)
- [Changelog](CHANGELOG.md)

### Development Setup
```bash
git clone https://github.com/your-username/PyEPISuite.git
cd PyEPISuite
pip install -e ".[dev]"
pytest  # Run tests
flake8 src tests  # Linting
mypy src  # Type checking
```

### Documentation
```bash
pip install -e ".[docs]"
mkdocs serve  # Local documentation server
```

## 📝 Citation

If you use PyEPISuite in your research, please cite:

```
Eftekhari, A. A. (2024). PyEPISuite: A Python client for EPA's EPISuite API 
with DataFrame utilities. https://github.com/USEtox/PyEPISuite
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- EPA for providing the EPISuite and EcoSAR APIs
- The pandas development team for the excellent DataFrame library
- All contributors and users of the package

## 🆕 What's New in v0.1.0

- ✨ **Complete DataFrame utilities** for data manipulation
- 📊 **Excel export functionality** with multi-sheet support
- 🧮 **Statistical analysis tools** and summary functions
- 📚 **Comprehensive documentation** with MkDocs
- 🧪 **Enhanced experimental data** access
- 🔧 **Improved API client** with better error handling
- 📈 **Advanced examples** for data analysis workflows

---

**API Reference**: See [EPISuite API Documentation](https://episuite.dev/EpiWebSuite/#/help/api) for the underlying web service.

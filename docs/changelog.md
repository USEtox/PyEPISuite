# Changelog

All notable changes to PyEPISuite will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete MkDocs documentation with Material theme
- Comprehensive user guides and examples
- API reference documentation

### Changed
- Improved code organization and structure
- Enhanced error handling and validation

## [0.1.0] - 2024-12-XX

### Added
- **DataFrame Utilities Module** (`dataframe_utils.py`)
  - `episuite_to_dataframe()` - Convert EPI Suite results to DataFrame
  - `ecosar_to_dataframe()` - Convert EcoSAR results to DataFrame
  - `episuite_experimental_to_dataframe()` - Extract experimental values
  - `combine_episuite_ecosar_dataframes()` - Merge datasets
  - `export_to_excel()` - Multi-sheet Excel export
  - `create_summary_statistics()` - Generate descriptive statistics

- **Enhanced Dependencies**
  - Added pandas (>=1.5.0) for DataFrame operations
  - Added openpyxl (>=3.0.0) for Excel export functionality

- **Documentation Infrastructure**
  - MkDocs configuration with Material theme
  - Comprehensive user guides and tutorials
  - Real-world examples and use cases
  - Complete API reference with auto-generated docs

- **New Features**
  - Structured data access with 41 EPI Suite properties
  - Support for 12 EcoSAR prediction columns
  - Experimental data extraction and validation
  - Multi-format export capabilities (Excel, CSV)
  - Statistical analysis utilities

### Enhanced
- **Core API Client** (`api_client.py`)
  - Improved error handling and timeout management
  - Better documentation and type hints

- **Utility Functions** (`utils.py`)
  - Enhanced CAS number validation
  - Robust batch processing support
  - Improved logging and error reporting

- **Data Models** (`models.py`)
  - Complete dataclass definitions for all API responses
  - Type-safe data structures
  - Comprehensive property coverage

### Documentation
- **Getting Started Guide**
  - Installation instructions
  - Quick start tutorial
  - Basic usage examples

- **User Guides**
  - API client usage
  - DataFrame utilities
  - Experimental data access

- **Examples**
  - Basic usage patterns
  - Advanced data analysis workflows
  - Batch processing scenarios

- **API Reference**
  - Complete function documentation
  - Parameter descriptions
  - Return value specifications
  - Usage examples

### Developer Experience
- **Type Safety**
  - Complete type hints throughout codebase
  - Type-safe DataFrame operations
  - Runtime type validation

- **Error Handling**
  - Graceful handling of API failures
  - Informative error messages
  - Fallback strategies for missing data

- **Performance**
  - Efficient DataFrame operations
  - Optimized API usage patterns
  - Memory-conscious data processing

## [0.0.1] - 2024-XX-XX

### Added
- Initial release
- Basic API client functionality
- Core data models
- Experimental data access
- Basic utility functions

### Features
- Search chemicals by CAS, SMILES, or name
- Submit chemicals for EPI Suite predictions
- Access EcoSAR ecotoxicity models
- Basic experimental data integration
- CAS number validation

---

## Version Comparison

### 0.1.0 vs 0.0.1 Improvements

| Feature | 0.0.1 | 0.1.0 |
|---------|-------|-------|
| **Data Format** | Raw dictionaries | Structured DataFrames |
| **Export Options** | JSON only | Excel, CSV, multiple sheets |
| **Documentation** | Basic README | Comprehensive docs site |
| **Type Safety** | Partial | Complete type hints |
| **Analysis Tools** | None | Statistical utilities |
| **Experimental Data** | Basic access | Structured extraction |
| **Error Handling** | Basic | Robust with fallbacks |
| **Examples** | Minimal | Real-world workflows |

### Migration Guide (0.0.1 → 0.1.0)

If upgrading from version 0.0.1:

#### New Requirements
```bash
pip install pandas>=1.5.0 openpyxl>=3.0.0
```

#### DataFrame Conversion
```python
# Old way (0.0.1)
results = submit_to_episuite(ids)
# Work with raw dictionary structures

# New way (0.1.0)
from pyepisuite.dataframe_utils import episuite_to_dataframe
epi_results, ecosar_results = submit_to_episuite(ids)
df = episuite_to_dataframe(epi_results)
```

#### Excel Export
```python
# New functionality in 0.1.0
from pyepisuite.dataframe_utils import export_to_excel
export_to_excel({
    'EPI_Results': epi_df,
    'EcoSAR_Results': ecosar_df
}, 'results.xlsx')
```

---

## Planned Features

### Version 0.2.0 (Planned)
- **Visualization Module**
  - Pre-built plotting functions
  - Interactive dashboards
  - Property correlation plots

- **Advanced Analysis**
  - QSAR model validation
  - Uncertainty quantification
  - Batch comparison tools

- **Integration Features**
  - ChemSpider integration
  - PubChem data access
  - OECD toolbox compatibility

### Version 0.3.0 (Planned)
- **Machine Learning Tools**
  - Property prediction models
  - Similarity analysis
  - Clustering algorithms

- **Regulatory Support**
  - REACH compliance checking
  - EPA guidelines integration
  - Risk assessment frameworks

---

## Breaking Changes

### None (0.1.0)
Version 0.1.0 maintains full backward compatibility with 0.0.1. All existing code will continue to work without modification.

---

## Contributors

### Version 0.1.0
- **Ali A. Eftekhari** - DataFrame utilities, documentation, testing

### Version 0.0.1
- **Ali A. Eftekhari** - Initial API client and core functionality

---

## Acknowledgments

- EPA for providing the EPISuite and EcoSAR APIs
- The pandas development team for the excellent DataFrame library
- The MkDocs community for documentation tools
- All users who provided feedback and feature requests

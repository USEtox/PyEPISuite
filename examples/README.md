# PyEPISuite Examples

This directory contains practical examples demonstrating how to use PyEPISuite for various workflows.

## Examples Overview

### 1. `cache_example.py`

Demonstrates the caching functionality for improved performance:

- 💾 Shows how caching works for submit_to_episuite
- ⚡ Compares cached vs non-cached performance
- 🗂️ Basic cache management operations

**Usage:**
```bash
python examples/cache_example.py
```

### 2. `comprehensive_cache_example.py`

A comprehensive demonstration of the full caching system:

- 💾 **Submit function caching** - Cache EPI Suite and EcoSAR results
- 🔍 **Search function caching** - Cache search results for CAS and general queries
- ⚡ **Performance comparisons** - Shows dramatic speedup from caching
- 🗂️ **Cache management** - Clear cache, view cache directory, count files
- 📊 **Logging output** - See exactly when cache is used

**Usage:**
```bash
python examples/comprehensive_cache_example.py
```

**Benefits demonstrated:**
- Drastically faster repeated operations
- Reduced API calls and network usage
- Persistent cache across Python sessions
- Automatic cache key generation

## Key Features Demonstrated

### Chemical Search and Data Retrieval
- Search chemicals by CAS numbers using `search_episuite_by_cas()`
- Handle CAS number formatting differences (EPI Suite returns zero-padded CAS, e.g. `000067-56-1`)
- Submit chemicals for EPI Suite predictions using `submit_to_episuite()`

### DataFrame Conversion
- Convert EPI Suite results to pandas DataFrame using `episuite_to_dataframe()`
- Access 120+ chemical properties in tabular format
- Convert EcoSAR results with `ecosar_to_dataframe()` and join them via
  `combine_episuite_ecosar_dataframes()`
- Handle missing values and data types properly

## Running the Examples

### Prerequisites

1. **Install PyEPISuite:**
   ```bash
   cd /path/to/PyEPISuite
   pip install -e .
   ```

2. **Required Python packages:**
   - pandas
   - openpyxl (for Excel export)
   - requests (for API calls)

## Troubleshooting

### Common Issues

1. **"No chemicals found in EPI Suite database"**
   - Check that CAS numbers are correctly formatted
   - Some chemicals may not be available in the EPI Suite database
   - Try alternative CAS number formats or SMILES strings

2. **Import errors**
   - Ensure PyEPISuite is properly installed: `pip install -e .`
   - Check that all required dependencies are installed
   - Run from the correct directory with proper Python path

### Getting Help

- Check the main PyEPISuite documentation
- Review the tutorial notebooks: `notebooks/tutorial01.ipynb` and `notebooks/tutorial_local.ipynb`
- Open an issue on the GitHub repository if you encounter problems

## Extending the Examples

You can easily modify these examples to:

- **Add more chemicals**: Extend the chemical list
- **Include EcoSAR data**: Use `ecosar_to_dataframe()` and combine results
- **Add experimental data**: Incorporate your own experimental measurements
- **Add data validation**: Implement additional quality checks

Example modification to add more chemicals:

```python
target_chemicals = [
    "67-56-1",    # Methanol
    "100-41-4",   # Ethylbenzene  
    "108-88-3",   # Toluene
    "71-43-2",    # Benzene
    "110-54-3",   # n-Hexane
    # Add your chemicals here...
]
```

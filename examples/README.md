# PyEPISuite Examples

This directory contains practical examples demonstrating how to use PyEPISuite for various workflows.

## Examples Overview

### 1. `simple_usetox_export.py` ⭐ **Recommended**

A complete, self-contained example that demonstrates the full workflow:

- ✅ **Works out of the box** - No external dependencies
- 🔍 Searches for chemicals by CAS numbers
- ⚗️ Gets EPI Suite predictions  
- 📊 Converts results to pandas DataFrame
- 📤 Exports to USEtox-compatible Excel format
- 📋 Creates multiple Excel sheets with different data views

**Usage:**
```bash
python examples/simple_usetox_export.py
```

**Output:**
- `pyepisuite_usetox_ready.xlsx` with three sheets:
  - `USEtox_Ready`: Properties formatted for USEtox software
  - `Full_EPI_Suite_Data`: Complete EPI Suite results (86 properties)
  - `Summary`: Export metadata and information

**Chemicals included in the example:**
- Methanol (CAS: 67-56-1)
- Ethylbenzene (CAS: 100-41-4) 
- Toluene (CAS: 108-88-3)

### 2. `cache_example.py`

Demonstrates the caching functionality for improved performance:

- 💾 Shows how caching works for submit_to_episuite
- ⚡ Compares cached vs non-cached performance
- 🗂️ Basic cache management operations

**Usage:**
```bash
python examples/cache_example.py
```

### 3. `comprehensive_cache_example.py` ⭐ **New**

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

### 4. `usetox_excel_example.py`

A more comprehensive example that demonstrates advanced USEtox integration:

- 🔧 Uses the full USEtoxInput class functionality
- 📊 Demonstrates experimental data prioritization
- 🗂️ Shows Excel column mapping
- ⚠️ Requires USEtox template files (may not work without setup)

**Usage:**
```bash
python examples/usetox_excel_example.py
```

**Note:** This example may fall back to basic Excel export if USEtox template files are not available.

## Key Features Demonstrated

### Chemical Search and Data Retrieval
- Search chemicals by CAS numbers using `search_episuite_by_cas()`
- Handle CAS number formatting differences (padding with zeros)
- Submit chemicals for EPI Suite predictions using `submit_to_episuite()`

### DataFrame Conversion
- Convert EPI Suite results to pandas DataFrame using `episuite_to_dataframe()`
- Access 86+ chemical properties in tabular format
- Handle missing values and data types properly

### USEtox Format Export
- Map PyEPISuite properties to USEtox-compatible column names
- Convert units where necessary (log values to linear, etc.)
- Create multiple Excel sheets for different data views
- Add metadata and data source tracking

### Properties Included in USEtox Export

| PyEPISuite Property | USEtox Column | Description |
|---------------------|---------------|-------------|
| `cas` | `CAS_RN` | Chemical registry number |
| `name` | `Chemical_Name` | Chemical name |
| `molecular_weight` | `MW_g_mol` | Molecular weight (g/mol) |
| `log_kow_estimated` | `Log_Kow` | Log octanol-water partition coefficient |
| `water_solubility_logkow_estimated` | `Solubility_mg_L` | Water solubility (mg/L) |
| `vapor_pressure_estimated` | `Vapor_Pressure_mmHg` | Vapor pressure (mmHg) |
| `henrys_law_constant_estimated` | `Henrys_Constant_atm_m3_mol` | Henry's law constant |
| `atmospheric_half_life_estimated` | `Atmospheric_Half_Life_hours` | Atmospheric degradation half-life |
| `log_koc_estimated` | `Log_Koc` | Log organic carbon-water partition coefficient |
| `bioconcentration_factor` | `BCF` | Bioconcentration factor |
| `river_half_life_hours` | `Water_Half_Life_hours` | Water degradation half-life |

**Derived columns:**
- `Kow`: Linear octanol-water partition coefficient (10^Log_Kow)
- `Koc`: Linear organic carbon-water partition coefficient (10^Log_Koc)
- `Data_Source`: Source of the data ("PyEPISuite_Estimated")

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

### Expected Output Files

After running the examples, you'll find these files in the `examples/` directory:

- `pyepisuite_usetox_ready.xlsx`: Multi-sheet Excel file with USEtox-ready data
- `episuite_results_fallback.xlsx`: Basic DataFrame export (if USEtox export fails)

## Using the Results

### For USEtox Software
1. Open the `pyepisuite_usetox_ready.xlsx` file
2. Use the `USEtox_Ready` sheet for importing into USEtox
3. Review the data and add any missing experimental values
4. Run USEtox calculations for environmental impact assessment

### For Further Analysis
1. Use the `Full_EPI_Suite_Data` sheet for comprehensive property analysis
2. Import the data into R, Python, or other analysis tools
3. Combine with experimental data or other databases
4. Perform statistical analysis or modeling

## Troubleshooting

### Common Issues

1. **"No chemicals found in EPI Suite database"**
   - Check that CAS numbers are correctly formatted
   - Some chemicals may not be available in the EPI Suite database
   - Try alternative CAS number formats or SMILES strings

2. **"USEtox export error"**
   - This is usually due to missing template files or unit conversion issues
   - The examples will fall back to basic Excel export
   - Use the basic export and manually format for USEtox if needed

3. **Import errors**
   - Ensure PyEPISuite is properly installed: `pip install -e .`
   - Check that all required dependencies are installed
   - Run from the correct directory with proper Python path

### Getting Help

- Check the main PyEPISuite documentation
- Review the tutorial notebook: `notebooks/tutorial01.ipynb`
- Open an issue on the GitHub repository if you encounter problems

## Extending the Examples

You can easily modify these examples to:

- **Add more chemicals**: Extend the `target_chemicals` list
- **Include EcoSAR data**: Use `ecosar_to_dataframe()` and combine results
- **Add experimental data**: Incorporate your own experimental measurements
- **Customize output format**: Modify column mappings and Excel formatting
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

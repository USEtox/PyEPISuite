# USEtox Integration

PyEPISuite includes comprehensive support for creating USEtox model input files from PyEPISuite API results.

## Overview

The USEtoxInput class provides functionality to:
- Load USEtox Excel templates
- Populate templates with PyEPISuite data
- Perform automatic unit conversions
- Add experimental data
- Validate data quality
- Export formatted Excel files

## Quick Start

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import episuite_to_dataframe
from pyepisuite.usetox_input import create_usetox_input_from_episuite

# Get PyEPISuite data
cas_list = ["50-00-0", "100-00-5", "100-02-7"]
ids = search_episuite_by_cas(cas_list)
epi_results, _ = submit_to_episuite(ids)
epi_df = episuite_to_dataframe(epi_results)

# Create USEtox input file (one-liner)
usetox_input = create_usetox_input_from_episuite(
    episuite_df=epi_df,
    output_path="my_usetox_input.xlsx"
)
```

## Step-by-Step Usage

### 1. Initialize USEtoxInput

```python
from pyepisuite.usetox_input import USEtoxInput

# Use default template
usetox_input = USEtoxInput()

# Or specify custom template path
usetox_input = USEtoxInput(template_path="path/to/custom/template.xlsx")
```

### 2. Populate with PyEPISuite Data

```python
# Populate the template
populated_df = usetox_input.populate_from_episuite_dataframe(episuite_df)

# View populated data
print(populated_df[['CAS RN', 'Name', 'MW', 'KOW', 'Koc']].head())
```

### 3. Add Experimental Data (Optional)

```python
experimental_data = {
    '50-00-0': {  # CAS number
        'Sol25': 400.0,  # Experimental solubility in g/L
        'Pvap25': 518700.0,  # Experimental vapor pressure in Pa
        'Data source': 'Experimental'
    }
}

usetox_input.populate_from_experimental_data(experimental_data)
```

### 4. Add Chemicals Manually (Optional)

```python
properties = {
    'MW': 78.11,
    'KOW': 100.0,  # Actual KOW value (not log)
    'Sol25': 1.78,  # g/L
    'Pvap25': 12700.0,  # Pa
}

row_index = usetox_input.add_chemical_manually(
    cas='71-43-2',
    name='Benzene',
    properties=properties
)
```

### 5. Validate Data

```python
validation = usetox_input.validate_data()

if validation['warnings']:
    print("Warnings:", validation['warnings'])
if validation['errors']:
    print("Errors:", validation['errors'])
```

### 6. Get Summary Statistics

```python
stats = usetox_input.get_summary_statistics()
print(f"Total chemicals: {stats['total_chemicals']}")
print("Property statistics:", stats['property_statistics'])
```

### 7. Export to Excel

```python
usetox_input.export_to_excel(
    output_path="usetox_input.xlsx",
    sheet_name="Substance inputs",
    include_headers=True,
    include_original_template=False
)
```

## Data Mapping and Unit Conversions

### Column Mapping

| PyEPISuite Column | USEtox Column | Unit Conversion |
|------------------|---------------|-----------------|
| `cas` | `CAS RN` | None |
| `name` | `Name` | None |
| `molecular_weight` | `MW` | None |
| `log_kow_estimated` | `KOW` | 10^(log KOW) |
| `log_koc_estimated` | `Koc` | 10^(log Koc) |
| `henrys_law_constant_estimated` | `KH25C` | None |
| `vapor_pressure_estimated` | `Pvap25` | mmHg → Pa (×133.322) |
| `water_solubility_logkow_estimated` | `Sol25` | mg/L → g/L (÷1000) |
| `atmospheric_half_life_estimated` | `T1/2A` | None |

### Automatic Unit Conversions

The class automatically handles unit conversions:

- **Log KOW → KOW**: Converts logarithmic values to actual values using 10^x
- **Log Koc → Koc**: Converts logarithmic values to actual values using 10^x  
- **Vapor Pressure**: Converts mmHg to Pa (×133.322)
- **Water Solubility**: Converts mg/L to g/L (÷1000)

## Data Validation

The validation system checks for:

### Warnings
- Missing CAS numbers
- Duplicate CAS numbers
- Extreme KOW values (< 1e-10 or > 1e10)

### Errors
- Negative molecular weights
- Invalid data types

## Integration with Experimental Data

You can combine PyEPISuite predictions with experimental data:

```python
# PyEPISuite provides predictions
# You provide experimental data to override/supplement
experimental_data = {
    'cas_number': {
        'property_name': experimental_value,
        'Data source': 'Experimental'
    }
}

usetox_input.populate_from_experimental_data(experimental_data)
```

## Excel Export Features

### Standard Export
- Creates properly formatted Excel file
- Includes column headers
- Compatible with USEtox software

### Advanced Export Options
```python
usetox_input.export_to_excel(
    output_path="advanced_export.xlsx",
    sheet_name="Substance inputs",
    include_headers=True,
    include_original_template=True  # Adds original template as separate sheet
)
```

### Excel Formatting
- Bold headers with gray background
- Title row with generation information
- Multiple sheets (data + original template)

## API Reference

### USEtoxInput Class

#### Constructor
```python
USEtoxInput(template_path: Optional[str] = None)
```

#### Main Methods
- `populate_from_episuite_dataframe(episuite_df, start_row=0, overwrite=True)`
- `populate_from_experimental_data(experimental_data, cas_column='CAS RN')`
- `add_chemical_manually(cas, name, properties, row_index=None)`
- `export_to_excel(output_path, sheet_name="Substance inputs", ...)`
- `get_summary_statistics()`
- `validate_data()`

#### Convenience Function
```python
create_usetox_input_from_episuite(
    episuite_df: pd.DataFrame,
    output_path: str,
    template_path: Optional[str] = None,
    experimental_data: Optional[Dict] = None
) -> USEtoxInput
```

## Examples

### Complete Workflow

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import episuite_to_dataframe
from pyepisuite.usetox_input import USEtoxInput

# 1. Get chemical data from PyEPISuite
cas_numbers = ["50-00-0", "71-43-2", "100-00-5"]
chemical_ids = search_episuite_by_cas(cas_numbers)
epi_results, ecosar_results = submit_to_episuite(chemical_ids)
epi_df = episuite_to_dataframe(epi_results)

# 2. Create USEtoxInput instance
usetox_input = USEtoxInput()

# 3. Populate with PyEPISuite data
usetox_input.populate_from_episuite_dataframe(epi_df)

# 4. Add experimental data
experimental_data = {
    "50-00-0": {"Sol25": 400.0, "Data source": "Experimental"}
}
usetox_input.populate_from_experimental_data(experimental_data)

# 5. Validate and get statistics
validation = usetox_input.validate_data()
stats = usetox_input.get_summary_statistics()

print(f"Created input for {stats['total_chemicals']} chemicals")
if validation['warnings']:
    print("Warnings:", validation['warnings'])

# 6. Export to Excel
usetox_input.export_to_excel("final_usetox_input.xlsx")
```

### Batch Processing

```python
# Process multiple chemical lists
chemical_batches = [
    ["50-00-0", "71-43-2"],
    ["100-00-5", "100-02-7"],
    ["111-65-9", "67-56-1"]
]

usetox_input = USEtoxInput()
row_offset = 0

for i, cas_batch in enumerate(chemical_batches):
    # Get data for this batch
    ids = search_episuite_by_cas(cas_batch)
    epi_results, _ = submit_to_episuite(ids)
    epi_df = episuite_to_dataframe(epi_results)
    
    # Add to USEtox template
    usetox_input.populate_from_episuite_dataframe(
        epi_df, 
        start_row=row_offset, 
        overwrite=False
    )
    row_offset += len(epi_df)

# Export combined results
usetox_input.export_to_excel("combined_batches.xlsx")
```

## Troubleshooting

### Common Issues

1. **Template not found**: Provide explicit template path
2. **Unit conversion errors**: Check for NaN or invalid values
3. **Excel export fails**: Ensure output directory exists and is writable
4. **Data validation warnings**: Review chemical properties for reasonableness

### Error Handling

```python
try:
    usetox_input = USEtoxInput(template_path="custom_template.xlsx")
    usetox_input.populate_from_episuite_dataframe(episuite_df)
    usetox_input.export_to_excel("output.xlsx")
except FileNotFoundError:
    print("Template file not found")
except ValueError as e:
    print(f"Data validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

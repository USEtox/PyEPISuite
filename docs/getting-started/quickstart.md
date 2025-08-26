# Quick Start Guide

This guide will get you up and running with PyEPISuite in just a few minutes.

## Basic Workflow

The typical PyEPISuite workflow involves three main steps:

1. **Search** for chemicals using identifiers
2. **Submit** chemicals to get predictions
3. **Convert** results to DataFrames for analysis

## Your First PyEPISuite Script

Let's start with a simple example that demonstrates the core functionality:

```python
from pyepisuite import (
    search_episuite_by_cas, 
    submit_to_episuite
)
from pyepisuite.dataframe_utils import (
    episuite_to_dataframe,
    ecosar_to_dataframe
)

# Step 1: Search for chemicals by CAS number
cas_numbers = ["50-00-0", "100-00-5", "100-02-7"]  # Formaldehyde, p-Nitroanisole, p-Nitrophenol
chemical_ids = search_episuite_by_cas(cas_numbers)

print(f"Found {len(chemical_ids)} chemicals")
for chem in chemical_ids:
    print(f"  {chem.name} (CAS: {chem.cas})")
```

```python
# Step 2: Submit chemicals for predictions
epi_results, ecosar_results = submit_to_episuite(chemical_ids)

print(f"\\nReceived predictions for {len(epi_results)} chemicals")
```

```python
# Step 3: Convert to DataFrames
epi_df = episuite_to_dataframe(epi_results)
ecosar_df = ecosar_to_dataframe(ecosar_results)

print(f"\\nEPI Suite DataFrame: {epi_df.shape[0]} chemicals × {epi_df.shape[1]} properties")
print(f"EcoSAR DataFrame: {ecosar_df.shape[0]} predictions × {ecosar_df.shape[1]} columns")

# Display some key properties
print("\\nKey Properties:")
properties = ['name', 'log_kow_estimated', 'water_solubility_logkow_estimated', 
              'bioconcentration_factor', 'atmospheric_half_life_estimated']
print(epi_df[properties].to_string(index=False))
```

## Working with Individual Results

You can also work with individual chemical results:

```python
# Access properties of the first chemical
chemical = epi_results[0]

print(f"Chemical: {chemical.chemicalProperties.name}")
print(f"CAS: {chemical.chemicalProperties.cas}")
print(f"Molecular Weight: {chemical.chemicalProperties.molecularWeight}")
print(f"Log Kow: {chemical.logKow.estimatedValue.value}")
print(f"Melting Point: {chemical.meltingPoint.estimatedValue.value} {chemical.meltingPoint.estimatedValue.units}")
```

## Searching by Different Identifiers

PyEPISuite supports multiple search methods:

### By CAS Numbers
```python
from pyepisuite import search_episuite_by_cas

cas_list = ["50-00-0", "67-56-1"]  # Formaldehyde, Methanol
results = search_episuite_by_cas(cas_list)
```

### By SMILES or Names
```python
from pyepisuite import search_episuite

# Search by SMILES
smiles_list = ["CCO", "C=O"]  # Ethanol, Formaldehyde
results = search_episuite(smiles_list)

# Search by name
names = ["benzene", "toluene"]
results = search_episuite(names)
```

## DataFrame Operations

Once you have DataFrames, you can perform various operations:

### Basic Statistics
```python
from pyepisuite.dataframe_utils import create_summary_statistics

# Get summary statistics for numeric columns
stats = create_summary_statistics(epi_df)
print(stats)
```

### Filtering and Selection
```python
# Select chemicals with high bioconcentration potential
high_bcf = epi_df[epi_df['log_bioconcentration_factor'] > 3]
print(f"Chemicals with log BCF > 3: {len(high_bcf)}")

# Select specific properties
key_properties = epi_df[['name', 'cas', 'log_kow_estimated', 'water_solubility_logkow_estimated']]
```

### Export to Excel
```python
from pyepisuite.dataframe_utils import export_to_excel

# Export multiple sheets to Excel
export_data = {
    'EPI_Suite_Results': epi_df,
    'EcoSAR_Results': ecosar_df,
    'Summary_Statistics': create_summary_statistics(epi_df)
}

export_to_excel(export_data, 'chemical_analysis.xlsx')
print("Data exported to chemical_analysis.xlsx")
```

## Working with Experimental Data

PyEPISuite also provides access to experimental datasets:

```python
from pyepisuite.expdata import HenryData, SolubilityData

# Load experimental data
henry_data = HenryData()
solubility_data = SolubilityData()

# Get experimental values for a specific chemical
cas = "50-00-0"  # Formaldehyde
henry_exp = henry_data.HLC(cas)
solubility_exp = solubility_data.solubility(cas)

print(f"Experimental Henry's Law Constant: {henry_exp}")
print(f"Experimental Solubility: {solubility_exp}")
```

## Error Handling

Always include error handling for robust applications:

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite

try:
    # Search for chemicals
    cas_list = ["50-00-0", "invalid-cas"]
    chemical_ids = search_episuite_by_cas(cas_list)
    
    # Submit for predictions
    epi_results, ecosar_results = submit_to_episuite(chemical_ids)
    
    print(f"Successfully processed {len(epi_results)} chemicals")
    
except Exception as e:
    print(f"Error: {e}")
    # Handle the error appropriately
```

## Next Steps

Now that you know the basics:

- Explore the [User Guide](../user-guide/api-client.md) for detailed explanations
- Check out [Examples](../examples/basic-usage.md) for real-world use cases
- Review the [API Reference](../api-reference/api-client.md) for complete documentation

## Common Patterns

Here are some patterns you'll use frequently:

### Batch Processing
```python
# Process multiple batches of chemicals
all_results = []
batch_size = 10

for i in range(0, len(large_cas_list), batch_size):
    batch = large_cas_list[i:i+batch_size]
    ids = search_episuite_by_cas(batch)
    results, _ = submit_to_episuite(ids)
    all_results.extend(results)

final_df = episuite_to_dataframe(all_results)
```

### Data Validation
```python
# Validate results before analysis
valid_results = []
for result in epi_results:
    if result.logKow.estimatedValue.value is not None:
        valid_results.append(result)

print(f"Valid results: {len(valid_results)}/{len(epi_results)}")
```

Ready to dive deeper? Head to the [User Guide](../user-guide/api-client.md)!

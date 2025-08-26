# Basic Usage Examples

This page provides practical examples of common PyEPISuite usage patterns.

## Single Chemical Analysis

### Getting Started with One Chemical

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite

# Step 1: Search for a chemical
cas = "50-00-0"  # Formaldehyde
ids = search_episuite_by_cas([cas])

print(f"Found chemical: {ids[0].name}")
print(f"SMILES: {ids[0].smiles}")

# Step 2: Get predictions
epi_results, ecosar_results = submit_to_episuite(ids)

# Step 3: Access specific properties
chemical = epi_results[0]
print(f"Log Kow: {chemical.logKow.estimatedValue.value}")
print(f"Water Solubility: {chemical.waterSolubilityFromLogKow.estimatedValue.value} {chemical.waterSolubilityFromLogKow.estimatedValue.units}")
```

### Converting to DataFrame for Analysis

```python
from pyepisuite.dataframe_utils import episuite_to_dataframe, ecosar_to_dataframe

# Convert to DataFrames
epi_df = episuite_to_dataframe(epi_results)
ecosar_df = ecosar_to_dataframe(ecosar_results)

# View chemical properties
print("\\nChemical Properties:")
print(epi_df[['name', 'cas', 'molecular_weight', 'log_kow_estimated']].to_string(index=False))

# View ecotoxicity predictions
print("\\nEcotoxicity Predictions:")
print(ecosar_df[['organism', 'endpoint', 'concentration']].to_string(index=False))
```

## Multiple Chemical Analysis

### Batch Processing

```python
# Define a set of chemicals
chemicals = [
    "50-00-0",   # Formaldehyde
    "67-56-1",   # Methanol  
    "64-17-5",   # Ethanol
    "67-64-1",   # Acetone
    "100-41-4"   # Ethylbenzene
]

# Process all chemicals
ids = search_episuite_by_cas(chemicals)
epi_results, ecosar_results = submit_to_episuite(ids)

# Convert to DataFrames
epi_df = episuite_to_dataframe(epi_results)
ecosar_df = ecosar_to_dataframe(ecosar_results)

print(f"Processed {len(epi_df)} chemicals")
print(f"Generated {len(ecosar_df)} ecotoxicity predictions")
```

### Property Comparison

```python
import matplotlib.pyplot as plt

# Compare key properties
properties = ['log_kow_estimated', 'water_solubility_logkow_estimated', 'log_bioconcentration_factor']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, prop in enumerate(properties):
    ax = axes[i]
    epi_df.plot(x='name', y=prop, kind='bar', ax=ax, legend=False)
    ax.set_title(prop.replace('_', ' ').title())
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```

## Working with Different Identifiers

### Search by SMILES

```python
from pyepisuite import search_episuite

# Search using SMILES strings
smiles_list = [
    "CCO",        # Ethanol
    "C=O",        # Formaldehyde  
    "CC(=O)C",    # Acetone
    "CCc1ccccc1"  # Ethylbenzene
]

ids = search_episuite(smiles_list)
epi_results, ecosar_results = submit_to_episuite(ids)

# Check what was found
for i, result in enumerate(epi_results):
    print(f"SMILES: {smiles_list[i]} -> {result.chemicalProperties.name}")
```

### Search by Name

```python
# Search by chemical names  
chemical_names = [
    "benzene",
    "toluene", 
    "xylene",
    "naphthalene"
]

ids = search_episuite(chemical_names)
print(f"Found {len(ids)} chemicals from {len(chemical_names)} names")

for id_obj in ids:
    print(f"  {id_obj.name} (CAS: {id_obj.cas})")
```

## Data Export and Visualization

### Excel Export

```python
from pyepisuite.dataframe_utils import export_to_excel, create_summary_statistics

# Prepare data for export
export_data = {
    'Chemical_Properties': epi_df[['name', 'cas', 'molecular_weight', 'molecular_formula']],
    'Physical_Properties': epi_df[['name', 'log_kow_estimated', 'water_solubility_logkow_estimated', 
                                   'vapor_pressure_estimated', 'henrys_law_constant_estimated']],
    'Environmental_Fate': epi_df[['name', 'atmospheric_half_life_estimated', 'bioconcentration_factor',
                                  'log_bioconcentration_factor']],
    'Ecotoxicity': ecosar_df,
    'Summary_Stats': create_summary_statistics(epi_df)
}

export_to_excel(export_data, 'chemical_analysis.xlsx')
print("Results exported to chemical_analysis.xlsx")
```

### Simple Visualization

```python
import seaborn as sns

# Create correlation plot
numeric_cols = ['log_kow_estimated', 'water_solubility_logkow_estimated', 
                'log_bioconcentration_factor', 'atmospheric_half_life_estimated']

correlation_matrix = epi_df[numeric_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Property Correlations')
plt.tight_layout()
plt.show()
```

## Error Handling Best Practices

### Robust Chemical Processing

```python
def process_chemicals_safely(cas_list):
    """Process chemicals with error handling."""
    successful_results = []
    failed_chemicals = []
    
    for cas in cas_list:
        try:
            # Search for chemical
            ids = search_episuite_by_cas([cas])
            
            if not ids:
                failed_chemicals.append({'cas': cas, 'error': 'Not found'})
                continue
                
            # Get predictions
            epi_results, ecosar_results = submit_to_episuite(ids)
            
            if epi_results:
                successful_results.extend(epi_results)
            else:
                failed_chemicals.append({'cas': cas, 'error': 'No predictions'})
                
        except Exception as e:
            failed_chemicals.append({'cas': cas, 'error': str(e)})
    
    return successful_results, failed_chemicals

# Usage
test_chemicals = ["50-00-0", "invalid-cas", "67-56-1", "another-invalid"]
results, failures = process_chemicals_safely(test_chemicals)

print(f"Successfully processed: {len(results)} chemicals")
print(f"Failed: {len(failures)} chemicals")

for failure in failures:
    print(f"  {failure['cas']}: {failure['error']}")
```

### Validating Results

```python
def validate_episuite_results(epi_df):
    """Validate EPI Suite results for completeness."""
    validation_report = {}
    
    # Check for missing critical properties
    critical_props = ['log_kow_estimated', 'water_solubility_logkow_estimated', 
                     'bioconcentration_factor']
    
    for prop in critical_props:
        missing_count = epi_df[prop].isna().sum()
        validation_report[prop] = {
            'missing_count': missing_count,
            'completion_rate': f"{(1 - missing_count/len(epi_df))*100:.1f}%"
        }
    
    return validation_report

# Usage
validation = validate_episuite_results(epi_df)
print("Data Completeness Report:")
for prop, stats in validation.items():
    print(f"  {prop}: {stats['completion_rate']} complete")
```

## Working with Experimental Data

### Model Validation

```python
from pyepisuite.expdata import HenryData, SolubilityData

# Load experimental data
henry_data = HenryData()
solubility_data = SolubilityData()

# Compare predictions with experimental values
validation_results = []

for _, row in epi_df.iterrows():
    cas = row['cas']
    name = row['name']
    
    # Get experimental values
    exp_henry = henry_data.HLC(cas)
    exp_solubility = solubility_data.solubility(cas)
    
    # Get predicted values
    pred_henry = row['henrys_law_constant_estimated']
    pred_solubility = row['water_solubility_logkow_estimated']
    
    if exp_henry and pred_henry:
        henry_ratio = pred_henry / exp_henry
        validation_results.append({
            'chemical': name,
            'property': 'Henry Law Constant',
            'predicted': pred_henry,
            'experimental': exp_henry,
            'ratio': henry_ratio
        })
    
    if exp_solubility and pred_solubility:
        solubility_ratio = pred_solubility / exp_solubility  
        validation_results.append({
            'chemical': name,
            'property': 'Water Solubility',
            'predicted': pred_solubility,
            'experimental': exp_solubility,
            'ratio': solubility_ratio
        })

# Display validation results
validation_df = pd.DataFrame(validation_results)
print("\\nModel Validation Results:")
print(validation_df.to_string(index=False))
```

## Next Steps

- Explore [Advanced Data Analysis](data-analysis.md) for sophisticated analysis workflows
- Learn about [Batch Processing](batch-processing.md) for large datasets  
- Check out the [DataFrame Utilities Guide](../user-guide/dataframe-utils.md) for more analysis options

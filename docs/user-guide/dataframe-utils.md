# DataFrame Utilities

The DataFrame utilities in PyEPISuite provide powerful tools for converting API results into pandas DataFrames, making it easy to analyze, manipulate, and export chemical data.

## Overview

The `dataframe_utils` module includes functions for:

- Converting EPI Suite results to DataFrames
- Converting EcoSAR results to DataFrames  
- Extracting experimental values
- Combining different datasets
- Exporting to Excel
- Generating summary statistics

## Core Functions

### Converting EPI Suite Results

The `episuite_to_dataframe()` function converts EPI Suite predictions into a structured DataFrame:

```python
from pyepisuite.dataframe_utils import episuite_to_dataframe

# Convert results to DataFrame
df = episuite_to_dataframe(epi_results)

print(f"DataFrame shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
```

#### Available Columns

The resulting DataFrame includes:

**Chemical Identifiers:**
- `cas`, `name`, `systematic_name`, `smiles`
- `molecular_weight`, `molecular_formula`

**Physical Properties:**
- `log_kow_estimated`, `melting_point_estimated`, `boiling_point_estimated`
- `vapor_pressure_estimated`, `water_solubility_*_estimated`
- `henrys_law_constant_estimated`, `log_koa_estimated`, `log_koc_estimated`

**Environmental Fate:**
- `atmospheric_half_life_estimated`, `aerosol_adsorption_fraction_estimated`
- `hydrocarbon_biodegradation_rate_estimated`

**Bioaccumulation:**
- `bioconcentration_factor`, `log_bioconcentration_factor`
- `bioaccumulation_factor`, `biotransformation_half_life`

**Other Properties:**
- `river_half_life_hours`, `lake_half_life_hours`
- `dermal_permeability_coefficient`, `fugacity_persistence`

### Converting EcoSAR Results

The `ecosar_to_dataframe()` function handles ecotoxicity predictions:

```python
from pyepisuite.dataframe_utils import ecosar_to_dataframe

# Convert EcoSAR results
ecosar_df = ecosar_to_dataframe(ecosar_results)

print(ecosar_df.groupby(['organism', 'endpoint']).size())
```

#### EcoSAR DataFrame Structure

- `cas`, `smiles` - Chemical identifiers
- `log_kow_input`, `water_solubility_input`, `melting_point_input` - Input parameters
- `qsar_class` - QSAR model class
- `organism` - Test organism (fish, daphnid, algae)
- `duration` - Test duration (acute, chronic)
- `endpoint` - Toxicity endpoint (LC50, EC50, ChV)
- `concentration` - Predicted concentration (mg/L)
- `max_log_kow` - Maximum log Kow for model applicability
- `flags` - Model applicability flags

## Working with Experimental Values

Extract experimental data for model validation:

```python
from pyepisuite.dataframe_utils import episuite_experimental_to_dataframe

# Get experimental values in long format
exp_df = episuite_experimental_to_dataframe(epi_results)

# Count experimental values by property
print(exp_df['property'].value_counts())

# Filter for specific properties
log_kow_exp = exp_df[exp_df['property'] == 'log_kow']
print(log_kow_exp[['name', 'value', 'author', 'year']])
```

## Combining Datasets

Merge EPI Suite and EcoSAR data for comprehensive analysis:

```python
from pyepisuite.dataframe_utils import combine_episuite_ecosar_dataframes

# Combine DataFrames
combined_df = combine_episuite_ecosar_dataframes(epi_df, ecosar_df)

print(f"Combined shape: {combined_df.shape}")

# The function automatically aggregates multiple EcoSAR results per chemical
print("EcoSAR summary columns:")
ecosar_cols = [col for col in combined_df.columns if 'concentration' in col or 'organism' in col]
print(ecosar_cols)
```

## Data Analysis Examples

### Property Correlations

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Select numeric properties for correlation analysis
numeric_props = [
    'log_kow_estimated', 'water_solubility_logkow_estimated',
    'log_bioconcentration_factor', 'atmospheric_half_life_estimated'
]

# Create correlation matrix
corr_matrix = epi_df[numeric_props].corr()

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Property Correlations')
plt.tight_layout()
plt.show()
```

### Property Distributions

```python
# Analyze property distributions
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

properties = [
    ('log_kow_estimated', 'Log Kow'),
    ('log_bioconcentration_factor', 'Log BCF'),
    ('atmospheric_half_life_estimated', 'Atmospheric Half-life (hours)'),
    ('water_solubility_logkow_estimated', 'Water Solubility (mg/L)')
]

for i, (prop, title) in enumerate(properties):
    ax = axes[i//2, i%2]
    epi_df[prop].hist(bins=20, ax=ax, alpha=0.7)
    ax.set_title(title)
    ax.set_ylabel('Frequency')

plt.tight_layout()
plt.show()
```

### Filtering by Criteria

```python
# Find chemicals meeting specific criteria
criteria = {
    'high_bcf': epi_df['log_bioconcentration_factor'] > 3,
    'persistent': epi_df['atmospheric_half_life_estimated'] > 48,
    'hydrophobic': epi_df['log_kow_estimated'] > 4
}

for name, condition in criteria.items():
    matching = epi_df[condition]
    print(f"{name.replace('_', ' ').title()}: {len(matching)} chemicals")
    if len(matching) > 0:
        print(f"  Examples: {', '.join(matching['name'].head(3))}")
```

## Export and Reporting

### Excel Export with Multiple Sheets

```python
from pyepisuite.dataframe_utils import export_to_excel, create_summary_statistics

# Prepare data for export
export_data = {
    'Chemical_Properties': epi_df[['name', 'cas', 'molecular_weight', 'log_kow_estimated']],
    'Environmental_Fate': epi_df[['name', 'cas', 'atmospheric_half_life_estimated', 
                                  'bioconcentration_factor']],
    'Ecotoxicity': ecosar_df,
    'Experimental_Values': exp_df,
    'Summary_Statistics': create_summary_statistics(epi_df)
}

export_to_excel(export_data, 'comprehensive_analysis.xlsx')
```

### Custom Reports

```python
# Create a summary report
report_df = epi_df.copy()

# Add classification columns
report_df['bcf_category'] = pd.cut(
    report_df['log_bioconcentration_factor'], 
    bins=[-np.inf, 2, 3, np.inf], 
    labels=['Low', 'Moderate', 'High']
)

report_df['persistence_category'] = pd.cut(
    report_df['atmospheric_half_life_estimated'],
    bins=[-np.inf, 24, 168, np.inf],
    labels=['Non-persistent', 'Moderately persistent', 'Persistent']
)

# Generate summary
summary = report_df.groupby(['bcf_category', 'persistence_category']).size().unstack(fill_value=0)
print("Chemical Classification Summary:")
print(summary)
```

## Advanced Operations

### Data Quality Assessment

```python
def assess_data_quality(df):
    """Assess data quality of EPI Suite results."""
    quality_report = {}
    
    # Check for missing values
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    quality_report['missing_data'] = missing_pct[missing_pct > 0].to_dict()
    
    # Check for outliers (using IQR method)
    numeric_cols = df.select_dtypes(include=['number']).columns
    outliers = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        if outlier_count > 0:
            outliers[col] = outlier_count
    
    quality_report['outliers'] = outliers
    
    return quality_report

# Assess quality
quality = assess_data_quality(epi_df)
print("Data Quality Report:")
for category, data in quality.items():
    print(f"\n{category.replace('_', ' ').title()}:")
    for item, value in data.items():
        print(f"  {item}: {value}")
```

### Batch Processing Large Datasets

```python
def process_large_dataset(cas_list, batch_size=50):
    """Process large datasets in batches."""
    all_epi_results = []
    all_ecosar_results = []
    
    for i in range(0, len(cas_list), batch_size):
        batch = cas_list[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(cas_list)-1)//batch_size + 1}")
        
        try:
            ids = search_episuite_by_cas(batch)
            epi_batch, ecosar_batch = submit_to_episuite(ids)
            
            all_epi_results.extend(epi_batch)
            all_ecosar_results.extend(ecosar_batch)
            
        except Exception as e:
            print(f"Error processing batch: {e}")
            continue
    
    return all_epi_results, all_ecosar_results

# Usage
# large_cas_list = [...]  # Your large list of CAS numbers
# epi_results, ecosar_results = process_large_dataset(large_cas_list)
```

## Best Practices

1. **Always check data types** after conversion:
   ```python
   print(df.dtypes)
   df.describe()
   ```

2. **Handle missing values** appropriately:
   ```python
   # Check missing data patterns
   missing_summary = df.isnull().sum()
   print(missing_summary[missing_summary > 0])
   ```

3. **Validate results** using experimental data:
   ```python
   # Compare estimated vs experimental values
   comparison = pd.merge(
       epi_df[['cas', 'log_kow_estimated']],
       exp_df[exp_df['property'] == 'log_kow'][['cas', 'value']],
       on='cas',
       suffixes=['_estimated', '_experimental']
   )
   ```

4. **Use appropriate data types** for analysis:
   ```python
   # Convert to appropriate types
   df['cas'] = df['cas'].astype('category')
   df['molecular_weight'] = pd.to_numeric(df['molecular_weight'], errors='coerce')
   ```

## Next Steps

- Explore the [Examples](../examples/data-analysis.md) for real-world analysis scenarios
- Check the [API Reference](../api-reference/dataframe-utils.md) for complete function documentation
- Learn about [Experimental Data](experimental-data.md) integration

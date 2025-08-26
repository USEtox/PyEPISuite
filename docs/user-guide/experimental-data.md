# Experimental Data

PyEPISuite provides access to curated experimental datasets for model validation and comparison.

## Overview

The experimental data module includes:

- Henry's Law Constants
- Boiling Points  
- Melting Points
- Vapor Pressures
- Water Solubility data

## Available Datasets

::: pyepisuite.expdata
    options:
      show_source: true
      show_root_heading: true

## Usage Examples

### Henry's Law Constants

```python
from pyepisuite.expdata import HenryData

# Load Henry's law constant data
henry = HenryData()

# Get value for a specific chemical
hlc = henry.HLC("50-00-0")  # Formaldehyde
print(f"Henry's Law Constant: {hlc}")

# Access the full dataset
df = henry.data
print(df.head())
```

### Solubility Data

```python
from pyepisuite.expdata import SolubilityData

# Load solubility data
solubility = SolubilityData()

# Get solubility for a chemical
sol = solubility.solubility("50-00-0")
print(f"Water Solubility: {sol}")
```

### Physical Properties

```python
from pyepisuite.expdata import (
    BoilingPointData,
    MeltingPointData, 
    VaporPressureData
)

# Load physical property data
bp_data = BoilingPointData()
mp_data = MeltingPointData()
vp_data = VaporPressureData()

# Get values
bp = bp_data.boiling_point("50-00-0")
mp = mp_data.melting_point("50-00-0")
vp = vp_data.vapor_pressure("50-00-0")
```

## Data Validation

Use experimental data to validate model predictions:

```python
from pyepisuite import search_episuite_by_cas, submit_to_episuite
from pyepisuite.dataframe_utils import episuite_to_dataframe
from pyepisuite.expdata import HenryData

# Get model predictions
cas_list = ["50-00-0", "67-56-1"]  # Formaldehyde, Methanol
ids = search_episuite_by_cas(cas_list)
epi_results, _ = submit_to_episuite(ids)
df = episuite_to_dataframe(epi_results)

# Get experimental data
henry = HenryData()

# Compare predictions vs experimental
for _, row in df.iterrows():
    cas = row['cas']
    predicted = row['henrys_law_constant_estimated']
    experimental = henry.HLC(cas)
    
    if experimental is not None:
        print(f"{row['name']} (CAS: {cas})")
        print(f"  Predicted: {predicted}")
        print(f"  Experimental: {experimental}")
        print(f"  Ratio: {predicted/experimental:.2f}")
```

## Data Sources

The experimental datasets are curated from:

- EPA's experimental databases
- Peer-reviewed literature
- Standard reference sources
- Quality-controlled measurements

## Data Quality

All experimental data includes:

- Source attribution
- Quality flags
- Uncertainty information where available
- Units and conditions

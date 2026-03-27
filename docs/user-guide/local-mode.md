# Local Runtime Mode

This guide explains how to run EPISuite locally with `EpiSuiteCLI.jar` and use it through `pyepisuite`.

## What Was Verified

The bundled JAR starts a local HTTP server and prints a dynamic port, for example:

```text
EPISuite started on http://127.0.0.1:45511/
```

The local API exposes OpenAPI JSON at:

- `GET /api`

The key endpoints are:

- `GET /api/search?query=...`
- `GET /api/submit?cas=...`
- `GET /api/submit?smiles=...`

## Prerequisites

- Java runtime available in `PATH`
- Local assets under `data/local/`
  - `EpiSuiteCLI.jar`
  - `EpiSearch.sqlite`
  - `EpiUnified.sqlite`
  - `AimExpKowwin.sqlite`

## Linux Setup

```bash
# Optional: force local mode
export PYEPISUITE_MODE=local

# Optional: custom startup timeout
export PYEPISUITE_LOCAL_STARTUP_TIMEOUT=90

# Optional: explicit JAR path
export PYEPISUITE_LOCAL_JAR_PATH=/absolute/path/to/EpiSuiteCLI.jar
```

Python usage:

```python
from pyepisuite import EpiSuiteAPIClient

client = EpiSuiteAPIClient()  # local-first in auto mode
hits = client.search("formaldehyde")
res = client.submit(cas="000050-00-0")
```

## Windows Setup (PowerShell)

```powershell
$env:PYEPISUITE_MODE = "local"
$env:PYEPISUITE_LOCAL_STARTUP_TIMEOUT = "90"
$env:PYEPISUITE_LOCAL_JAR_PATH = "C:\path\to\EpiSuiteCLI.jar"
```

Python usage:

```python
from pyepisuite import LocalEpiSuiteAPIClient

client = LocalEpiSuiteAPIClient()
hits = client.search("formaldehyde")
res = client.submit(cas="000050-00-0")
```

## Local vs Remote Selection

- `PYEPISUITE_MODE=auto` (default): local-first when local JAR is present
- `PYEPISUITE_MODE=local`: require local runtime
- `PYEPISUITE_MODE=remote`: always use hosted API

## CAS Format Note

The local submit endpoint can reject unpadded CAS values like `50-00-0` and accept `000050-00-0`.

The client includes a local-mode retry that normalizes CAS prefix padding automatically.

## Runtime Troubleshooting

- `Java runtime not found in PATH`
  - Install Java and ensure `java` is available.
- `Failed to start local EpiSuite server and detect startup URL`
  - Increase `PYEPISUITE_LOCAL_STARTUP_TIMEOUT`
  - Run JAR manually and inspect startup logs.
- Non-JSON response from submit/search
  - Usually indicates invalid local input or endpoint error text returned as plain text.

## SQLite Databases (Inspection Only)

These databases are not yet wired into the API layer directly.

### EpiSearch.sqlite

- Table: `ChemicalNames` (115305 rows)
- Core columns: `Name`, `SystematicName`, `SMILES`, `CAS`, `ExpDataKey`, `CanonicalSmiles`
- Useful indexes: `ChemicalNames_Name_index`, `ChemicalNames_CAS_index`, `idx_ChemicalNames_CanonicalSmiles`

### AimExpKowwin.sqlite

- Table: `AimExpKowwin` (16146 rows)
- Table: `KowTrainingSet` (2365 rows)

### EpiUnified.sqlite

- Main table: `ChemicalProperties` (115573 rows)
- Property tables include:
  - `OctanolWaterPartitions`
  - `WaterSolubility`
  - `VaporPressures`
  - `MeltingPoints`
  - `BoilingPoints`
  - `HenryLaw`
  - `BioConcentrations`

Example inspection queries:

```sql
-- exact chemical lookup
SELECT Name, CAS, SMILES FROM ChemicalProperties WHERE CAS = '000050-00-0';

-- top search hits by name pattern
SELECT Name, CAS FROM ChemicalNames WHERE Name LIKE '%FORMALDEHYDE%' LIMIT 20;

-- property join pattern
SELECT cp.CAS, cp.Name, ow.Coefficient AS logKow, ws.Value AS water_solubility
FROM ChemicalProperties cp
LEFT JOIN OctanolWaterPartitions ow ON ow.Id = cp.KOW
LEFT JOIN WaterSolubility ws ON ws.Id = cp.WS
WHERE cp.CAS = '000050-00-0';
```

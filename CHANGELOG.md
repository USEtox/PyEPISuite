# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Widespread `dacite` parsing failures** (`missing value for field ...` / `wrong value type
  for field ...`) when submitting compounds to the EPI Suite API. Nearly every field in
  `models.py` lacked a default value, so any compound for which the API omitted a key or
  returned `null` (very common — modules can partially fail or skip compartments) crashed
  parsing instead of degrading gracefully. All ~530 dataclass fields are now `Optional` with a
  `None` default.
- **`fugacityModel.model.Air`/`Water`/`Soil`/`Sediment`** are now `Optional[List[...]]` instead
  of required lists, since these compartments can be entirely absent from the response for some
  compounds.
- **`AtmosphericHalfLifeParameters.hydroxylRadicalConcentration` / `.ozoneConcentration`** and
  every numeric/boolean field on `*Parameters` dataclasses (`WaterVolatilizationParameters`,
  `SewageTreatmentModelParameters`, `FugacityModelParameters`, `DermalPermeabilityParameters`,
  `HenrysLawConstantParameters`, `LogKoaParameters`, `LogKocParameters`,
  `BioconcentrationParameters`, `AerosolAdsorptionFractionParameters`,
  `WaterSolubilityFromLogKowParameters`, `EcosarParameters`, and the top-level `Parameters`)
  now accept either a raw scalar or a full `Parameter` object (`{value, units, source,
  valueType}`), matching the API's actual behavior of echoing user-supplied inputs as plain
  values but defaulted/derived inputs as provenance-carrying objects.
- **`LogKocEstimatedValue.model` / `waterVolatilization.parameters` mismatches** where the API's
  internal shape didn't match the previous rigid dataclasses (e.g. `logKoc` model returned as a
  list instead of an object for some compounds).
- Internal, non-contractual `model` breakdown fields on estimated values (`logKow`,
  `meltingPoint`, `boilingPoint`, `vaporPressure`, `waterSolubility*`, `logKoa`, `logKoc`,
  `hydrocarbonBiodegradationRate`, `aerosolAdsorptionFraction`, `atmosphericHalfLife`) are no
  longer part of the API's documented contract (per the OpenAPI spec at
  https://episuite.dev/api, only `HenryEstimatedValue.model` is contractually defined) and vary
  in shape across compounds. These fields now use a typed-first, raw-fallback `Union` so
  existing attribute-based access keeps working for the common case while no longer crashing
  when the API returns an unexpected shape.
- Added a `source` field to `Parameter` so provenance metadata from the API is no longer
  silently dropped.
- `dataframe_utils.py`: fixed `AttributeError`/`TypeError` crashes (e.g.
  `'NoneType' object has no attribute 'Percent'`) caused by `hasattr(dataclass_instance, attr)`
  checks that are always `True` regardless of whether the field's value is `None`. Replaced the
  risky chained-attribute accesses (sewage treatment removal percentages, fugacity persistence
  and half-life arrays, biodegradation model names) with proper `None` checks.

## [1.2.0] - 2026-04-23

### Added
- **Automatic JAR download** — `_LocalRuntimeManager` now automatically downloads `EpiSuiteCLI.jar`
  from `https://episuite.dev/api/download` when the file is not present locally, eliminating the
  need for manual installation. The download URL can be overridden via the
  `PYEPISUITE_JAR_DOWNLOAD_URL` environment variable.
- **Download progress bar** — a `tqdm`-based progress bar is shown during the JAR download,
  displaying transferred size, speed, and estimated time remaining.
- **`tqdm>=4.0.0`** added as a runtime dependency.

## [1.1.0] - 2026-04-16

### Added
- **Local mode support** via embedded Java executable (EpiSuiteCLI.jar) for offline EPISuite calculations
- Local API client that starts and communicates with the local Java server

### Changed
- Switched project tooling to `uv` for faster dependency management
- Updated DataFrame utilities with additional properties
- Dropped Python 3.10 support; minimum version is now Python 3.11

### Fixed
- Type issue and typo fixes

## [1.0.0] - 2025-08-29

### Added
- **Comprehensive DataFrame utilities** for converting EPI Suite and EcoSAR results to pandas DataFrames
- **45+ properties** extracted from EPI Suite results including:
  - Chemical identification and classification
  - Physical-chemical properties (Log Kow, melting/boiling points, solubility, etc.)
  - Environmental fate (atmospheric half-life, biodegradation, bioconcentration)
  - Detailed atmospheric chemistry (hydroxyl radical and ozone reaction rates)
  - Bioconcentration with trophic level data
  - Water volatilization parameters
  - Dermal permeability coefficients
  - Fugacity model persistence and compartment half-lives
  - Sewage treatment removal efficiencies
  - Hydrolysis rate constants
- **Excel export functionality** with multiple sheets and formatting
- **Summary statistics generation** for results analysis
- **Comprehensive MkDocs documentation** with API references and examples
- **GitHub Actions workflows** for automated testing and documentation deployment
- **Dependabot configuration** for automated dependency updates
- **Contributing guidelines**, security policy, and issue templates
- **Experimental data integration** for model validation

### Enhanced
- Updated package structure with improved organization
- Enhanced test coverage with comprehensive test cases
- Improved error handling and data validation
- Updated README with detailed usage examples and badges

### Infrastructure
- Complete CI/CD pipeline with GitHub Actions
- Documentation deployment to GitHub Pages
- Automated testing across multiple Python versions and operating systems
- Code quality checks with linting and type checking

## [0.1.0] - Initial Development

### Added
- Basic EPI Suite API client functionality
- Models for EPI Suite data structures
- Utility functions for common operations
- Experimental data handling capabilities
- Initial test suite
- Basic documentation

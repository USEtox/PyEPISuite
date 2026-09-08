# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2026-09-08

### Fixed
- **`expdata` raised `FileNotFoundError` on every installed copy of the package.**
  `data_folder()` resolved the CSVs as `<package>/../../data`, which is
  `site-packages/data` once installed and only ever existed in a source checkout.
  The wheel shipped no data at all, and although the sdist carried `data/`, it
  installed only `src/pyepisuite`, so it failed the same way. Every class in the
  module was affected: `HenryData`, `BoilingPointData`, `MeltingPointData`,
  `VaporPressureData`, `SolubilityData` and `logKowData`. This has been broken
  since at least 1.1.0.

  The eight runtime CSVs are now mapped into the wheel at `pyepisuite/data/`
  (`[tool.hatch.build.targets.wheel.force-include]`), and `data_folder()` prefers
  that packaged copy, falling back to the repo-root `data/` for source checkouts.
  The wheel grows from 30 KB to ~955 KB.

### Changed
- The sdist no longer sweeps in the whole repository. It drops the `.xls`/`.doc`
  source material, the `bcfbaf` and `waternt` trees that nothing reads, and the
  `notebooks/`, `docs/` and `examples/` directories, going from 8.2 MB to ~1.1 MB.
  The eight runtime CSVs stay, since the wheel build reads them.

### Removed
- `MANIFEST.in`. It is a setuptools file and this project builds with hatchling,
  which never read it — the 1.3.0 sdist contained `notebooks/` and `docs/`, which
  the file does not list, while its `recursive-include data *` had no effect on
  the wheel. Keeping it only suggested the data question was already handled.

## [1.3.0] - 2026-09-08

Targets **EPI Suite 1.1.0** (`pyepisuite.__episuite_version__`). The package version stays on its own
semver track; the EPI Suite version it speaks to is declared in metadata.

### Changed
- **Migrated the response models to the EPI Suite API v1.1.0 schema.** PR #11 pointed the
  client at `https://episuite.dev/api`, which serves a different API version than the models
  described. Because that PR also made every field `Optional` with a `None` default, the
  mismatch parsed "successfully" and silently produced `None` instead of raising, so whole
  sections came back empty. The models now follow the OpenAPI 3.0.3 spec the server publishes
  at `GET /api` (`info.version` 1.1.0), validated against captured responses for 11 compounds
  with zero unmapped keys.

  Response-shape changes, all of which previously yielded empty columns:
  - `sewageTreatmentModel.model` is now `{processBreakdown[], estimates}` with
    `estimates.totalRemovalPercent` and friends, replacing the `TotalRemoval.Percent`
    component tree (no key overlap with the old shape).
  - `fugacityModel.model` is now `{compartments[], estimates}`; per-compartment half-lives are
    `compartments[].halfLifeHours` keyed by `name`, replacing the fixed-order `HalfLifeArray`
    and the `Air`/`Water`/`Soil`/`Sediment` lists. Persistence is `estimates.persistenceHours`.
  - `biodegradationRate.models[]` reports `nativeValue` and `calculatedValue` instead of
    `value`, plus `shortName` (e.g. `biowin1`) and `formula`.
  - `hydrolysis` is reported per pathway and reactive site. The flat `acidCatalyzedRateConstant`
    / `baseCatalyzedRateConstant` / `neutralRateConstant` fields now live under `rates`, and
    `halfLives[]` carry their `mechanism` and `pH`. A new `disposition` field distinguishes
    "not hydrolyzable" from "no estimate".
  - `bioconcentration.arnotGobasBcfBafEstimates[]` are titled rows (`title`, `value`,
    `logValue`, `unit`) rather than a per-trophic-level breakdown.
  - Experimental and selected values share one `Value` schema, which gained `source`, `method`,
    `evidenceType`, `sourceDatabase`, `sourceTable`, `sourceId`, `referenceId`, `temperatureC`
    and `pressureMmHg`. `Parameter`, `ExperimentalValue` and `SelectedValue` are kept as
    aliases of it so existing attribute access still works.
  - Fragment counts are `count`/`maxCount` in KOCWIN and BIOWIN but remain
    `fragmentCount`/`maxFragmentCount` in KOWWIN, WSKOW, WATERNT, HENRYWIN and the hydrocarbon
    biodegradation model; each factor class now matches its own module.
  - `henrysLawConstant.estimatedValue.model[]` uses `hlcAtmM3PerMol`/`hlcPaM3PerMol` instead of
    `hlcAtm`/`hlcPaMol`, and reports `complete`, `unavailableReason` and `missingValues`.
  - `Parameters` now lists the v1.1.0 submit inputs; the 30 `user*` fields the current API never
    populates were removed.

### Added
- `pyepisuite.__episuite_version__` (and `episuite_version.EPISUITE_VERSION`) declares the
  EPI Suite version a release targets. It is the single source of truth: the cache namespace
  and the local-runtime jar floor both derive from it, so bumping it is the only edit needed
  when EPI Suite moves.
- **Local-runtime jar version check.** `read_jar_version` reads `Implementation-Version` from
  the jar manifest (a zip entry read, no JVM start) and `jar_is_supported` compares it against
  the minimum. A stale jar found on disk is now replaced with a warning instead of being
  launched and failing with the jar's own usage text; a jar named explicitly through
  `PYEPISUITE_LOCAL_JAR_PATH` is never replaced silently and raises an actionable error
  instead. `has_local_assets` no longer counts an unsupported jar, so `PYEPISUITE_MODE=auto`
  falls back to the remote API rather than failing to start.
- **Module-level error reporting.** Any module can come back as `{module, code, message}`
  instead of a result, so every module on `ResultEPISuite` is typed
  `Optional[Union[ModuleError, <result>]]`, and the top-level `errors` list is captured.
  `ModuleError`'s fields are required so `dacite` can tell an error apart from a real result.
  Check with `isinstance(result.fugacityModel, ModuleError)`. `episuite_to_dataframe` adds a
  `failed_modules` column, so a module that could not run is visible instead of just empty.
- New response sections: `ecosar` and the nine typed ECOSAR submodels,
  `fishBiotransformationRate`, and `analogIdentification` (which now carries the `analogs` and
  `logKowAnalogs` lists that used to sit at the top level).
- `utils.normalize_response_keys` rewrites the API's dotted keys
  (`"ecosar.nonionic-surfactant"`) to valid Python identifiers
  (`ecosar_nonionic_surfactant`) before parsing.
- New dataframe columns: fugacity compartment mass percentages and `fugacity_selected_koc`,
  per-mechanism hydrolysis half-lives and `hydrolysis_disposition`, titled Arnot-Gobas
  estimates, and `source`/`source_database`/`temperature_c` on the experimental long table.
- Tests that parse the captured `data/sample/result.json` and assert no response key is left
  unmapped, so a future schema drift fails the suite instead of silently emptying columns.

### Fixed
- `episuite_experimental_to_dataframe` crashed with `AttributeError` on a null
  `chemicalProperties` and `TypeError: 'NoneType' object is not iterable` when a property was
  present but its `experimentalValues` was absent. Both predate PR #11 but became reachable
  once partial responses started parsing.
- Cache keys are namespaced by `RESPONSE_SCHEMA_VERSION`, so entries written under the previous
  response shape are ignored rather than loaded into the current models. Mixing the two was
  what made the drift hard to spot: cached old-shape records still filled columns that a fresh
  response left empty.
- Removed the `Optional[str]` dacite hook that joined list values into `"a; b"`. It was
  compensating for `notes` being modelled as a string; those fields are `List[str]` in the
  API and are now typed that way, so the text is preserved instead of being flattened.

### Changed
- **Raised the minimum Python to 3.12** (`requires-python = ">=3.12"`, was `>=3.11`), and the
  CI test matrix now runs 3.12 only instead of 3.10/3.11/3.12 — the older interpreters were
  failing constantly. The `docs` and `release` workflows moved from 3.11 to 3.12 as well, since
  a 3.11 runner can no longer `pip install -e .`.

### Removed
- **The USEtox integration**, to keep the package a clean EPI Suite interface. This drops
  `pyepisuite.usetox_input` (the `USEtoxInput` class and the `create_usetox_input_from_*`
  helpers, also removed from the top-level `pyepisuite` namespace), its tests, the
  `usetox_excel_example.py` / `simple_usetox_export.py` / `simple_usetox_template.py`
  examples, the USEtox pages in the docs and the USEtox section of `notebooks/tutorial01.ipynb`.
  The `data/usetox3/` USEtox template is removed with it. Building the USEtox input from an
  `episuite_to_dataframe()` frame is a downstream concern, and the code had drifted: it
  documented `populate_from_experimental_data()` and `add_chemical_manually()` methods that
  did not exist, and read DataFrame columns (`sediment_half_life_hours`,
  `soil_half_life_hours`, `water_biodegradation_half_life_unacclimated`) that
  `episuite_to_dataframe()` has never produced, so several USEtox columns silently exported
  blank.

### Notes
- `data/sample/result.json` and `result_ecosar.json` were re-captured from v1.1.0.
- Local mode requires the current `epi` CLI jar (`epi-estimators-cli.jar`, reported as v1.1.0),
  which is what `https://episuite.dev/api/download` serves. A pre-existing
  `data/local/EpiSuiteCLI.jar` from the older 331 MB EpiSuiteCLI build is used as-is if present
  and does not support `--serve`, so replace it when upgrading.

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

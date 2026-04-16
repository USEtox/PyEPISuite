# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

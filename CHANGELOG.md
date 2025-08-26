# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- DataFrame utilities for converting EPI Suite and EcoSAR results to pandas DataFrames
- Excel export functionality with multiple sheets and formatting
- Summary statistics generation for results
- Comprehensive MkDocs documentation with API references
- GitHub Actions workflows for automated testing and documentation deployment
- Dependabot configuration for automated dependency updates
- Contributing guidelines and issue templates
- Security policy
- Pull request template

### Changed
- Updated package structure to include new DataFrame utilities
- Enhanced requirements with pandas and openpyxl dependencies
- Improved test coverage with new test cases
- Updated README with new features and usage examples

### Dependencies
- Added pandas (>=1.5.0)
- Added openpyxl (>=3.0.0)
- Added mkdocs and related documentation packages

## [1.0.0] - Initial Release

### Added
- Basic EPI Suite API client functionality
- Models for EPI Suite data structures
- Utility functions for common operations
- Experimental data handling capabilities
- Initial test suite
- Basic documentation

### Features
- EPI Suite API integration
- Result parsing and validation
- Error handling and logging
- Extensible model system

# GitHub Actions Release Setup

This document explains the automated release system for PyEPISuite using GitHub Actions.

## Overview

The release system consists of three main workflows:

1. **Tests** (`.github/workflows/test.yml`) - Runs tests on every push/PR
2. **Release** (`.github/workflows/release.yml`) - Builds and publishes packages
3. **Create Release** (`.github/workflows/create-release.yml`) - Creates GitHub releases from tags

## Setup Requirements

### 1. PyPI Trusted Publishing

To publish to PyPI automatically, you need to set up PyPI Trusted Publishing:

1. Go to [PyPI](https://pypi.org) and log in
2. Navigate to your project settings (or create the project first)
3. Go to "Publishing" → "Add a new pending publisher"
4. Fill in:
   - **PyPI project name**: `pyepisuite`
   - **Owner**: `USEtox` (your GitHub username/org)
   - **Repository name**: `PyEPISuite`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi`

### 2. GitHub Repository Settings

Ensure these settings in your GitHub repository:

1. **Actions**: Enable GitHub Actions (Settings → Actions → General)
2. **Environments**: Create a `pypi` environment (Settings → Environments)
3. **Permissions**: Ensure workflows can write to repository (Settings → Actions → General → Workflow permissions)

## Release Process

### Method 1: Using the Release Script (Recommended)

1. **Install the script dependencies** (if any):
   ```bash
   # The script only uses standard library, no additional dependencies needed
   ```

2. **Run the release script**:
   ```bash
   # Update version and create tag
   python scripts/release.py 1.0.1
   
   # Just show current version
   python scripts/release.py --current
   
   # Create tag for current version (if you already updated manually)
   python scripts/release.py --tag-only
   ```

3. **What the script does**:
   - Updates version in `src/pyepisuite/__init__.py`
   - Updates version in `pyproject.toml`
   - Commits the changes
   - Creates and pushes a git tag
   - Triggers the automated workflows

### Method 2: Manual Process

1. **Update version numbers**:
   ```bash
   # Edit src/pyepisuite/__init__.py
   __version__ = "1.0.1"
   
   # Edit pyproject.toml
   version = "1.0.1"
   ```

2. **Commit and push changes**:
   ```bash
   git add src/pyepisuite/__init__.py pyproject.toml
   git commit -m "Bump version to 1.0.1"
   git push origin main
   ```

3. **Create and push tag**:
   ```bash
   git tag -a v1.0.1 -m "Release 1.0.1"
   git push origin v1.0.1
   ```

### Method 3: GitHub UI

1. Update version numbers (manually or via PR)
2. Go to GitHub → Releases → "Create a new release"
3. Create a new tag (e.g., `v1.0.1`)
4. Add release notes
5. Publish the release

## What Happens Automatically

When you push a tag or create a release:

1. **Test Workflow** runs:
   - Installs dependencies
   - Runs pytest tests
   - Runs linting checks

2. **Build Workflow** runs:
   - Builds wheel and source distributions
   - Verifies the packages
   - Uploads build artifacts

3. **Release Workflow** runs:
   - Downloads build artifacts
   - Publishes to PyPI (using trusted publishing)
   - Attaches distribution files to GitHub release

4. **GitHub Release** is created:
   - Release notes from CHANGELOG.md (if available)
   - Distribution files (.whl and .tar.gz) attached

## Workflow Files Explained

### `.github/workflows/test.yml`
- Runs on: push, PR, releases
- Tests multiple Python versions (3.9-3.12)
- Tests multiple OS (Ubuntu, Windows, macOS)
- Includes linting and type checking

### `.github/workflows/release.yml`
- Runs on: releases and manual trigger
- Builds packages with `python -m build`
- Publishes to PyPI using trusted publishing
- Uploads assets to GitHub release

### `.github/workflows/create-release.yml`
- Runs on: version tags (v*.*.*)
- Creates GitHub releases automatically
- Extracts release notes from CHANGELOG.md
- Handles pre-release detection

## Troubleshooting

### PyPI Publishing Fails

1. **Check trusted publishing setup**: Ensure the PyPI trusted publisher is correctly configured
2. **Check environment name**: Must match exactly (`pypi`)
3. **Check workflow name**: Must be `release.yml`
4. **Check permissions**: Workflow needs `id-token: write`

### Tests Fail

1. **Check test dependencies**: Ensure all test dependencies are in `pyproject.toml`
2. **Check Python versions**: Tests run on 3.9-3.12
3. **Check OS compatibility**: Tests run on Ubuntu, Windows, macOS

### Release Not Created

1. **Check tag format**: Must be `v*.*.*` (e.g., `v1.0.0`)
2. **Check permissions**: Workflow needs `contents: write`
3. **Check branch**: Make sure you're on the main branch

## Security Notes

- **No secrets required**: Uses PyPI trusted publishing
- **Minimal permissions**: Workflows only get necessary permissions
- **Audit trail**: All releases are traceable through Git history

## Version Naming Convention

Follow semantic versioning:
- **Major**: `1.0.0` → `2.0.0` (breaking changes)
- **Minor**: `1.0.0` → `1.1.0` (new features)
- **Patch**: `1.0.0` → `1.0.1` (bug fixes)
- **Pre-release**: `1.0.0-beta1`, `1.0.0-rc1`

## Changelog Management

Keep `CHANGELOG.md` updated with:
```markdown
## [1.0.1] - 2025-08-29

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Change description
```

The release workflow will automatically extract the appropriate section for release notes.

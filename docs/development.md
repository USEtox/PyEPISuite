# Development Guide

This guide covers the development workflow, release process, and PyPI publishing for PyEPISuite.

## 🛠️ Development Setup

### 1. Clone and Install for Development

```bash
# Clone the repository
git clone https://github.com/USEtox/PyEPISuite.git
cd PyEPISuite

# Install in development mode with all dependencies
pip install -e ".[dev,docs]"
```

### 2. Development Dependencies

The development environment includes:
- **Testing**: pytest, pytest-cov
- **Code Quality**: black, isort, mypy, flake8
- **Documentation**: mkdocs, mkdocs-material, mkdocstrings

## 🧪 Testing and Quality Assurance

### Run Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/pyepisuite --cov-report=html

# Run specific test file
pytest tests/test_api_client.py
```

### Code Formatting and Linting
```bash
# Format code with black
black src tests

# Sort imports with isort
isort src tests

# Lint with flake8
flake8 src tests

# Type checking with mypy
mypy src
```

### Pre-commit Checks
Run all quality checks before committing:
```bash
# Format and lint
black src tests
isort src tests
flake8 src tests
mypy src

# Run tests
pytest --cov=src/pyepisuite
```

## 📚 Documentation

### Local Development
```bash
# Start local documentation server
mkdocs serve

# Build documentation
mkdocs build
```

### Documentation Structure
- `docs/` - Main documentation source
- `mkdocs.yml` - Documentation configuration
- Auto-generated API docs from docstrings

## 🚀 Release Process

### 1. Prepare for Release

1. **Update Version Number**
   ```bash
   # Edit pyproject.toml
   # Update version = "x.y.z"
   ```

2. **Update Changelog**
   ```bash
   # Edit CHANGELOG.md
   # Add new version section with changes
   ```

3. **Run Full Test Suite**
   ```bash
   # Ensure all tests pass
   pytest --cov=src/pyepisuite
   
   # Run quality checks
   black src tests
   isort src tests
   flake8 src tests
   mypy src
   ```

4. **Test Installation**
   ```bash
   # Test local installation
   pip install -e .
   python -c "import pyepisuite; print(pyepisuite.__version__)"
   ```

### 2. Create Release on GitHub

1. **Commit and Push Changes**
   ```bash
   git add .
   git commit -m "Prepare release v0.1.0"
   git push origin main
   ```

2. **Create GitHub Release**
   - Go to https://github.com/USEtox/PyEPISuite/releases
   - Click "Create a new release"
   - Tag version: `v0.1.0` (matching pyproject.toml version)
   - Release title: `PyEPISuite v0.1.0`
   - Add release notes from CHANGELOG.md
   - Click "Publish release"

3. **Automated Publishing**
   - GitHub Actions will automatically trigger
   - Package will be built and published to PyPI
   - Monitor the workflow at: https://github.com/USEtox/PyEPISuite/actions

## 📦 PyPI Publishing Setup

### 1. PyPI Account Setup

1. **Create PyPI Account**
   - Register at https://pypi.org/account/register/
   - Verify email address

2. **Create TestPyPI Account**
   - Register at https://test.pypi.org/account/register/
   - This is for testing releases

### 2. GitHub Repository Configuration

1. **Set up Trusted Publishing**
   - Go to PyPI → Account Settings → API tokens
   - Create a new "Pending publisher" for your repository:
     - PyPI Project Name: `pyepisuite`
     - Owner: `USEtox`
     - Repository: `PyEPISuite`
     - Workflow: `publish.yml`
     - Environment: `pypi`

2. **GitHub Environments**
   - Go to repository Settings → Environments
   - Create environments:
     - `pypi` (for production releases)
     - `testpypi` (for testing)
   - Add protection rules if desired

### 3. Manual Publishing (Alternative)

If you need to publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## 🔄 Workflow Options

### Automatic Release (Recommended)
1. Update version in `pyproject.toml`
2. Create GitHub release
3. Publishing happens automatically

### Manual Testing
1. Use workflow_dispatch to publish to TestPyPI
2. Test installation: `pip install -i https://test.pypi.org/simple/ pyepisuite`
3. Create release for PyPI publishing

### Emergency Hotfix
1. Create hotfix branch
2. Make necessary changes
3. Update version (patch increment)
4. Create release directly from hotfix branch

## 📋 Release Checklist

### Pre-Release
- [ ] All tests pass locally
- [ ] Code formatted and linted
- [ ] Version updated in `pyproject.toml`
- [ ] Changelog updated
- [ ] Documentation builds successfully
- [ ] Breaking changes documented

### Release
- [ ] GitHub release created with proper tag
- [ ] Release notes include all changes
- [ ] Automated workflow completed successfully
- [ ] Package available on PyPI
- [ ] Installation tested: `pip install pyepisuite`

### Post-Release
- [ ] Announcement on relevant channels
- [ ] Documentation deployed
- [ ] Version bump for next development cycle
- [ ] Known issues documented

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**
   ```bash
   # Check build locally
   python -m build
   # Fix any import or dependency issues
   ```

2. **Tests Fail in CI**
   ```bash
   # Run tests in same Python versions as CI
   pytest --cov=src/pyepisuite
   ```

3. **PyPI Upload Fails**
   - Check version number isn't already used
   - Verify trusted publishing is configured
   - Check GitHub environment settings

4. **Import Errors After Installation**
   ```bash
   # Verify package structure
   pip show pyepisuite
   # Check if data files are included
   ```

### Getting Help

- Check GitHub Actions logs for detailed error messages
- Review PyPI upload logs
- Open an issue on GitHub for persistent problems

## 🔧 Advanced Configuration

### Custom Build Configuration

Edit `pyproject.toml` for custom build settings:

```toml
[tool.setuptools.package-data]
pyepisuite = ["data/**/*"]

[tool.setuptools.exclude-package-data]
pyepisuite = ["*.pyc", "__pycache__"]
```

### Development Scripts

Add to `pyproject.toml`:

```toml
[project.scripts]
pyepisuite-cli = "pyepisuite.cli:main"
```

### Environment Variables

For local development:
```bash
# Set environment variables
export PYEPISUITE_DEBUG=1
export PYEPISUITE_API_URL=https://episuite.dev/api
```

---

## 📞 Support

For development questions:
- Open an issue on GitHub
- Check existing documentation
- Review similar projects for patterns

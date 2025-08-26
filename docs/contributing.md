# Contributing to PyEPISuite

Thank you for your interest in contributing to PyEPISuite! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/PyEPISuite.git
   cd PyEPISuite
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### Development Dependencies

The development environment includes:
- `pytest` - Testing framework
- `black` - Code formatting
- `isort` - Import sorting
- `mypy` - Type checking
- `flake8` - Linting
- `pre-commit` - Git hooks
- `mkdocs` - Documentation

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues. When creating a bug report, include:

- **Clear description** of the problem
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Actual behavior**
- **Environment details** (Python version, OS, etc.)
- **Error messages** or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear description** of the enhancement
- **Use case** or motivation
- **Possible implementation** approach
- **Examples** of how it would be used

### Code Contributions

#### Types of Contributions

We welcome contributions in these areas:

1. **New Features**
   - Additional DataFrame utilities
   - New data analysis functions
   - API enhancements
   - Integration with other tools

2. **Bug Fixes**
   - Fixing existing issues
   - Improving error handling
   - Performance improvements

3. **Documentation**
   - Improving existing docs
   - Adding examples
   - API documentation
   - Tutorials

4. **Tests**
   - Adding test coverage
   - Improving test quality
   - Performance tests

#### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Check code quality:**
   ```bash
   black .
   isort .
   flake8
   mypy src/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Coding Standards

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

### Code Organization

```
src/pyepisuite/
├── __init__.py          # Package initialization
├── api_client.py        # API communication
├── models.py            # Data models
├── utils.py             # Core utilities
├── dataframe_utils.py   # DataFrame conversion
└── expdata.py           # Experimental data
```

### Naming Conventions

- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private members**: `_leading_underscore`

### Documentation

- Use **Google-style docstrings**
- Include **type hints** for all functions
- Add **examples** in docstrings where helpful
- Keep docstrings **concise but complete**

Example function:
```python
def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert between different units.
    
    Args:
        value: The numeric value to convert
        from_unit: Source unit (e.g., 'mg/L')
        to_unit: Target unit (e.g., 'mol/L')
        
    Returns:
        The converted value
        
    Raises:
        ValueError: If units are not recognized
        
    Example:
        >>> convert_units(100, 'mg/L', 'g/L')
        0.1
    """
```

## Testing

### Writing Tests

- Use **pytest** for testing
- Follow **AAA pattern** (Arrange, Act, Assert)
- Test **both success and failure** cases
- Use **descriptive test names**
- Mock **external dependencies**

Example test:
```python
def test_episuite_to_dataframe_with_valid_results():
    """Test DataFrame conversion with valid EPI Suite results."""
    # Arrange
    mock_results = [create_mock_episuite_result()]
    
    # Act
    df = episuite_to_dataframe(mock_results)
    
    # Assert
    assert len(df) == 1
    assert 'cas' in df.columns
    assert df.iloc[0]['name'] == 'Test Chemical'
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyepisuite

# Run specific test file
pytest tests/test_dataframe_utils.py

# Run specific test
pytest tests/test_dataframe_utils.py::test_episuite_to_dataframe
```

## Documentation

### Building Documentation

```bash
# Install docs dependencies
pip install mkdocs mkdocs-material mkdocstrings[python]

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

### Documentation Structure

- **Getting Started**: Installation and quick start
- **User Guide**: Detailed usage instructions
- **Examples**: Real-world usage scenarios
- **API Reference**: Complete API documentation

### Writing Documentation

- Use **clear, concise language**
- Include **code examples**
- Provide **context and motivation**
- Link to **related concepts**
- Keep examples **up to date**

## Release Process

### Version Management

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Update documentation
5. Create release tag
6. Build and upload to PyPI

## Community Guidelines

### Code of Conduct

Please be respectful and constructive in all interactions. We're committed to providing a welcoming environment for all contributors.

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions

### Getting Help

If you need help:

1. Check the **documentation**
2. Search **existing issues**
3. Ask in **GitHub Discussions**
4. Create a **new issue** if needed

## Development Tips

### Working with the API

- Use **rate limiting** to avoid overwhelming the server
- Implement **retry logic** for transient failures
- Cache responses when appropriate
- Handle **network errors** gracefully

### DataFrame Utilities

- Always handle **missing values**
- Use **appropriate data types**
- Include **unit information**
- Validate **input data**

### Performance Considerations

- Profile code for **bottlenecks**
- Use **vectorized operations** in pandas
- Minimize **API calls**
- Consider **memory usage** for large datasets

## Recognition

All contributors will be acknowledged in the project documentation. Significant contributions may be recognized in release notes.

Thank you for contributing to PyEPISuite!

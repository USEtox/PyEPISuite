# Contributing to PyEPISuite

Thank you for your interest in contributing to PyEPISuite! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/PyEPISuite.git
   cd PyEPISuite
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write descriptive docstrings for all functions and classes
- Keep line length under 88 characters (Black default)

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting a PR:
  ```bash
  pytest
  ```
- Run linting and type checking:
  ```bash
  flake8 src tests
  mypy src
  ```

## Documentation

- Update documentation for any new features
- Test documentation builds locally:
  ```bash
  mkdocs serve
  ```
- Ensure all docstrings are complete and accurate

## Submitting Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Add tests for your changes
4. Update documentation if needed
5. Run the test suite
6. Commit your changes with a descriptive commit message
7. Push to your fork and submit a pull request

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure CI checks pass
- Be responsive to feedback

## Reporting Issues

When reporting issues, please include:

- Python version
- PyEPISuite version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages (if any)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## Questions?

If you have questions about contributing, feel free to open an issue or reach out to the maintainers.

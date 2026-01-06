# Contributing to img-optimize

Thank you for considering contributing to img-optimize! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs. **actual behavior**
- **Screenshots** if applicable
- **Environment details**: OS, Python version, img-optimize version
- **Sample images** (if safe to share)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case** and rationale
- **Detailed description** of the proposed functionality
- **Alternative solutions** you've considered
- **Mockups or examples** if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the development setup** instructions below
3. **Make your changes** with clear, descriptive commits
4. **Add tests** for new functionality
5. **Ensure tests pass** and code quality checks succeed
6. **Update documentation** including README and docstrings
7. **Submit your pull request** with a clear description

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/img-optimize.git
cd img-optimize

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=img_optimize --cov-report=html

# Run specific test file
pytest tests/test_optimizer.py

# Run with verbose output
pytest -v
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code with black
black src/ tests/

# Check code style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/

# Run pre-commit checks manually
pre-commit run --all-files
```

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all function signatures
- Write descriptive docstrings (Google style)
- Keep functions focused and modular
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Example Docstring Format

```python
def optimize_image(input_path: Path, quality: int = 85) -> Optional[Dict]:
    """Optimize a single image file.

    Args:
        input_path: Path to the input image file
        quality: JPEG quality setting (1-100)

    Returns:
        Dictionary with optimization results or None if failed

    Raises:
        ValueError: If quality is out of range
        FileNotFoundError: If input_path doesn't exist

    Examples:
        >>> result = optimize_image(Path("photo.jpg"), quality=90)
        >>> print(result['optimized_size'])
        524288
    """
```

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally after the first line

Examples:
```
Add WebP format support

Implement WebP optimization with quality settings.
Add tests for WebP file handling.
Closes #42
```

```
Fix recursive directory structure preservation

Update process_batch to use relative_to() for maintaining
directory hierarchy in output folder.
Fixes #38
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Aim for high test coverage (>80%)
- Test edge cases and error conditions
- Use descriptive test names

```python
def test_optimize_jpeg_with_custom_quality():
    """Test JPEG optimization with non-default quality setting."""
    # Arrange
    optimizer = ImageOptimizer(quality=75)
    # Act
    result = optimizer.optimize_image(input_path, output_path)
    # Assert
    assert result is not None
    assert result['optimized_size'] < result['original_size']
```

### Test Organization

```
tests/
├── test_cli.py          # CLI interface tests
├── test_optimizer.py    # Core optimization logic tests
├── test_utils.py        # Utility function tests
└── fixtures/            # Test data and fixtures
```

## Project Structure

```
img-optimize/
├── src/
│   └── img_optimize/
│       ├── __init__.py       # Package initialization
│       ├── cli.py            # Command-line interface
│       ├── optimizer.py      # Image optimization engine
│       └── utils.py          # Helper utilities
├── tests/                    # Test suite
├── .github/                  # GitHub workflows and templates
├── docs/                     # Additional documentation
├── pyproject.toml            # Project configuration
├── requirements.txt          # Production dependencies
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # This file
└── README.md                 # Project overview
```

## Adding New Features

When adding new features:

1. **Discuss first** - Open an issue to discuss major changes
2. **Branch naming** - Use descriptive names like `feature/webp-support` or `fix/recursive-bug`
3. **Keep it focused** - One feature/fix per PR
4. **Update docs** - Add to README, update help text, add examples
5. **Add tests** - Test the happy path and edge cases
6. **Update CHANGELOG** - Add entry under [Unreleased]

## Release Process

Maintainers follow this process for releases:

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md with release date
3. Create git tag: `git tag -a v2.0.0 -m "Release v2.0.0"`
4. Push tag: `git push origin v2.0.0`
5. GitHub Actions will build and publish to PyPI

## Questions?

- Check the [README](README.md) for basic usage
- Search [existing issues](https://github.com/onamfc/img-optimize/issues)
- Open a new issue with the "question" label

Thank you for contributing to img-optimize!

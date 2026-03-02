"""
This file contains development and contribution guidelines for the backtesting engine.
"""

## Development Guidelines

### Code Style

We follow PEP 8 for Python code style. Some key points:

- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters
- Use docstrings for all public classes and functions
- Use type hints where appropriate

### Documentation

All public classes and methods should be documented with docstrings following the Google style:

```python
def function_with_types_in_docstring(param1: int, param2: str) -> bool:
    """Example function with types documented in the docstring.
    
    Args:
        param1: The first parameter.
        param2: The second parameter.
        
    Returns:
        True if successful, False otherwise.
    """
```

### Testing

We use unittest for testing. All new functionality should have corresponding tests:

1. Create tests in the `tests` directory
2. Run tests using `python -m unittest discover tests`
3. Ensure all tests pass before submitting a pull request

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite to ensure all tests pass
6. Update documentation if necessary
7. Submit a pull request

### Version Control

We use semantic versioning:

- MAJOR version for incompatible API changes
- MINOR version for added functionality in a backward-compatible manner
- PATCH version for backward-compatible bug fixes

## Project Structure

```
backtesting_engine/
├── backtesting_engine/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_ingestion.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py
│   │   ├── moving_average.py
│   │   └── rsi_strategy.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── reporting.py
│   ├── engine.py
│   ├── metrics.py
│   └── simulation.py
├── examples/
│   ├── ma_crossover_example.py
│   └── strategy_comparison_example.py
├── tests/
│   ├── test_backtesting_engine.py
│   ├── test_metrics.py
│   └── test_strategies.py
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── setup.py
└── requirements.txt
```

## Adding a New Strategy

To add a new strategy:

1. Create a new file in the `strategies` directory
2. Subclass the `Strategy` base class
3. Implement the `generate_signals` method
4. Add tests for your strategy
5. Update the `__init__.py` file to expose your strategy
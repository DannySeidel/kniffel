# Kniffel

## Used Software Versions
- Python 3.10.2
- Pylint 2.13.5

## Used Libraries
- Pickle
- Hashlib
- Hmac
- Pytest
- Pytest-cov

## Pytest

### Install Pytest
```shell
pip install pytest
```

### Install Pytest-Cov
```shell
pip install pytest-cov
```

Run all tests with:
```shell
pytest
```

Run tests for one file:
```shell
pytest tests/"filename"
```

Run tests with coverage:
```shell
pytest --cov src
```

Run tests and save coverage to html files:
````shell
pytest --cov src --cov-report=html
````


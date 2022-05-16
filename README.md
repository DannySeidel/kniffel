# Kniffel
[![Pylint](https://github.com/DannySeidel/kniffel/actions/workflows/pylint.yml/badge.svg)](https://github.com/DannySeidel/kniffel/actions/workflows/pylint.yml)
[![Pytest](https://github.com/DannySeidel/kniffel/actions/workflows/pytest.yml/badge.svg)](https://github.com/DannySeidel/kniffel/actions/workflows/pytest.yml)

This Repository contains the game Kniffel / Yahtzee.\
The game can be played by two human players.\
If all thirteen turns are over it will return to the main menu.

The code was written by:
- Joshua Miller
- Tobias Welti
- Luca Kaiser
- Danny Seidel

To start the game you need the files:
- main.py
- game.py
- formatting.py
- error_handler.py

Additionally, the Repository includes tests for the above listed files:
- test_main.py
- test_game.py
- test_player.py
- test_error_handler.py

To ensure readable code pylint was used.\
The slightly adjusted config can be found in the .pylintrc file.

Furthermore, the project includes a pytest.ini file used by pytest.


## Used Software Versions
- Python 3.10.2
- Pylint 2.13.5

## Used Libraries
- Pickle
- Hashlib
- Hmac
- Pytest
- Pytest-cov

## Run Game
In the project root folder run:
```shell
python src/main.py
```

## Pytest

### Install Pytest
```shell
pip install pytest
```

### Install Pytest-Cov
```shell
pip install pytest-cov
```

### Run Tests

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


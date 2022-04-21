"""
kniffel
main.py

created on 06.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

from enum import Enum


class Color(str, Enum):
    """contains data for coloring the output"""

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Text(str, Enum):
    """contains text styles"""

    IMPORTANT = Color.BOLD + Color.RED
    REGULAR = Color.BOLD + Color.BLUE
    TURN = Color.BOLD + Color.PURPLE
    PLAYER = Color.BOLD + Color.CYAN
    DICE = Color.BOLD + Color.GREEN
    SCORE = Color.BOLD + Color.YELLOW


class Dice(str, Enum):
    """contains dice symbols"""

    ONE = f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █          █
    █    ██    █
    █          █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """

    TWO = f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █  ▄▄      █
    █  ▀▀  ▄▄  █
    █      ▀▀  █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """

    THREE = f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █ ██       █
    █    ██    █
    █       ██ █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """

    FOUR = f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █  ██  ██  █
    █          █
    █  ██  ██  █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """

    FIVES = f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █ ██    ██ █
    █    ██    █
    █ ██    ██ █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """

    SIX = f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █  ▀▀  ▀▀  █
    █  ██  ██  █
    █  ▄▄  ▄▄  █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """

"""
kniffel
main.py

created on 06.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import json
import os
import uuid
import game


def clear_console():
    """clears console based on operating system"""
    os.system("cls" if os.name == "nt" else "clear")


class Ui:
    """handles ui"""


if __name__ == "__main__":
    clear_console()
    game.Game.print_menu()
    game.Game.menu_input()

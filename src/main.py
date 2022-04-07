"""
kniffel
main.py

created on 06.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""
import json
import os
import sys
import uuid

import game


def clear_console():
    """clears console based on operating system"""
    os.system("cls" if os.name == "nt" else "clear")


def print_menu():
    """prints main menu"""
    print("Welcome to Yahtzee!\n")
    print("Start game (s)")
    print("Load game (l)")
    print("Quit (q)")


def menu_input():
    """handles inputs for main menu"""
    action = input("\nEnter action: ")

    if action == "s":
        pass
    elif action == "l":
        pass
    elif action == "q":
        sys.exit(0)
    else:
        pass


class Ui:
    def __init__(self):
        self.current_game = None

    def create_game(self):
        """..."""
        game_id = uuid.uuid4()
        self.current_game = game.Game(game_id)

    def save_game(self):
        """saves game date to json file"""
        with open("games.json", "w") as file:
            json.dump(self.current_game, file)

    def load_game(self):
        """loads game date from json file"""
        with open("games.json", "r") as file:
            data = json.load(file)
            game_id = data["uuid"]
            self.current_game = game.Game(game_id)


if __name__ == "__main__":
    clear_console()
    print_menu()
    menu_input()

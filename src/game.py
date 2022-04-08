"""
kniffel
game.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import player


class Game:
    """handles game data"""
    def __init__(self, uuid):
        self.uuid = uuid
        self.player_1 = player.Player(1)
        self.player_2 = player.Player(2)

    def create_new_game(self):
        """..."""
        input("Press enter to start a new game.")
        self.player_1.name = input("Please enter the name of player 1: ")
        self.player_2.name = input("Please enter the name of player 2: ")

    def load_game(self):
        input("Press enter to create a new game")

    def get_current_turn(self):
        """..."""


    def play_round(self):
        """..."""

    def get_winner(self) -> int:
        """returns id of the winner"""

"""
kniffel
game.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import player
import uuid
import json


class Game:
    """handles game data"""
    def __init__(self, uuid):
        self.uuid = uuid
        self.player_1 = player.Player(1)
        self.player_2 = player.Player(2)
        self.current_game = None
        self.current_turn = None

    def create_new_game(self):
        """..."""
        input("Press enter to start a new game.")
        game_id = uuid.uuid4()
        self.current_game = Game(game_id)
        self.player_1.name = input("Please enter the name of player 1: ")
        self.player_2.name = input("Please enter the name of player 2: ")
        self.current_turn = 0,
        self.current_game.current_turn = self.current_turn

    def save_game_state(self):
        """saves game date to json file//joshuas part"""

        with open("games.json", "w", encoding="utf-8") as file:
            json.dump(self.current_game, file)

    def load_game_state(self):
        """loads exisiting game state from json file"""

        input("Hello, please select a game to load.")
        input("Press enter to start the game.")
        with open("games.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            game_id = data["uuid"]
            self.current_game = Game(game_id)

    def play_round(self):
        """..."""

    def get_current_turn(self):
        """get the current turn of the game"""
        print(f'The current turn is {self.current_turn}')


    def get_winner(self) -> int:
        """returns id of the winner"""

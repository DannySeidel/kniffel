"""
kniffel
game.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import player
import uuid
import json
import sys


class Game:
    """handles game data"""

    def __init__(self, uuid):
        self.uuid = uuid
        self.player_1 = player.Player(1)
        self.player_2 = player.Player(2)
        self.current_game = None
        self.current_turn = None


    def print_menu():
        """prints main menu"""
        print("Welcome to Yahtzee!\n")
        print("Start new game (s)")
        print("Load existing game (l)")
        print("Quit (q)")

    def menu_input():
        """handles inputs for main menu"""
        action = input("\nEnter action: ")

        if action == "s":
            Game.create_new_game()
        elif action == "l":
            Game.load_game_state()
        elif action == "q":
            sys.exit(0)
        else:
            pass


    def create_new_game(self):
        """..."""
        input("Press enter to start a new game.")
        game_id = uuid.uuid4()
        self.current_game = Game(game_id)
        self.current_game.player_1 = input("Please enter the name of player 1: ")
        self.current_game.player_2 = input("Please enter the name of player 2: ")
        self.current_game.current_turn = 0
        self.current_game.save_game_state()
        self.current_game.play_game()


    def play_game(self):
        """starts game"""
        for i in range (13):
            self.current_game.play_round()
            self.current_game.save_game_state()

        self.current_game.print_winner()


    def play_round(self):
        """..."""
        """NOTE: better --> saving the current turn of each player and not the round"""
        self.current_game.print_round()
        self.current_turn = self.current_turn + 1
        self.current_game.current_turn = self.current_turn

        input(f"{self.current_game.player_1} it's your turn! Please enter to roll the first dices.")
        self.current_game.player_1.throw_dice(5)
        self.current_game.player_1.print_dices()
        self.current_game.player_1.dice_put_aside()

        input(f"{self.current_game.player_2} it's your turn! Please enter to roll the first dices.")
        self.current_game.player_2.throw_dice(5)
        self.current_game.player_2.print_dices()
        self.current_game.player_2.dice_put_aside()

        self.current_game.player_1.calculate_score()
        self.current_game.player_2.calculate_score()


    def get_current_turn(self):
        """get the current turn of the game"""
        print(f'The current turn is {self.current_turn}')
        return self.current_turn


    def get_winner(self) -> int:
        """returns id of the winner"""
        if self.player_1.score > self.player_2.score:
            return 1
        elif self.player_1.score < self.player_2.score:
            return 2


    def save_game_state(self):
        """saves game date to json file // joshuas part"""

        with open("games.json", "w", encoding="utf-8") as file:
            json.dump(self.current_game, file)


    def load_game_state(self):
        """loads exisiting game state from json file //joshuas part"""

        input("Hello, please select a game to load.")
        with open("games.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            game_id = data["uuid"]
            self.current_game = Game(game_id)

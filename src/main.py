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
    print("Start new game (s)")
    print("Load game (l)")
    print("Quit (q)")


def menu_input():
    """handles inputs for main menu"""
    action = input("\nEnter action: ")

    if action == "s":
        ui.create_new_game()
        ui.play_game()
    elif action == "l":
        ui.load_game()
        # ui.play_game()
    elif action == "q":
        sys.exit(0)
    else:
        pass


class Ui:
    """handles ui data"""
    def __init__(self):
        self.current_game = None

    def create_new_game(self):
        """..."""
        game_id = uuid.uuid4()
        self.current_game = game.Game(game_id)

    def play_game(self):
        """..."""
        turn = self.current_game.get_current_turn()
        while turn < 13:
            self.player_action(1)
            self.player_action(2)
            self.save_game()
            turn += 1

    def player_action(self, player_id):
        """..."""
        if player_id == 1:
            player = self.current_game.player_1
        else:
            player = self.current_game.player_2

        print(f"Player {player_id} is on:")
        attempt = 1
        player.dice_put_aside = []
        while attempt <= 3 and len(player.dice_put_aside) != 5:
            player.throw_dice()
            if attempt < 3:
                print(f"Your thrown {player.dice_used}.")
                if len(player.dice_put_aside) > 0:
                    print(f"Your have {player.dice_put_aside} put aside.")
                    player.reuse_dice()
                for value in player.dice_used:
                    print(f"Do you want rethrow the dice with current value {value}?")
                    action = input("Enter action (y/n): ")
                    if action == "n":
                        player.put_dice_aside(value)
                attempt += 1
            else:
                for value in player.dice_used:
                    player.put_dice_aside(value)

        self.save_round_score(player)

    def save_round_score(self, player):
        """..."""
        scores = player.get_all_possible_scores()

        print(f"You have thrown {player.dice_put_aside}.")
        print("Your scores are:")
        print("  Upper Section:")
        print(f"  1) Ones:             {scores[0]}")
        print(f"  2) Twos:             {scores[1]}")
        print(f"  3) Threes:           {scores[2]}")
        print(f"  4) Fours:            {scores[3]}")
        print(f"  5) Fives:            {scores[4]}")
        print(f"  6) Sixes:            {scores[5]}")
        print("  Lower Section:")
        print(f"  7) Three of a Kind:  {scores[6]}")
        print(f"  8) Four of a Kind:   {scores[7]}")
        print(f"  9) Full House:       {scores[8]}")
        print(f"  10) Small Straight:  {scores[9]}")
        print(f"  11) Large Straight:  {scores[10]}")
        print(f"  12) Yahtzee:         {scores[11]}")
        print(f"  13) Chance:          {scores[12]}")

        score_number = input("Enter the matching number to save the score: ")

        if score_number == 1:
            pass
        # ...

    def save_game(self):
        """saves game date to json file"""
        with open("games.json", "w", encoding="utf-8") as file:
            json.dump(self.current_game, file)

    def load_game(self):
        """loads game date from json file"""
        with open("games.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            game_id = data["uuid"]
            self.current_game = game.Game(game_id)


if __name__ == "__main__":
    clear_console()
    ui = Ui()
    print_menu()
    menu_input()

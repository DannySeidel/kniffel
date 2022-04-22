"""
kniffel
main.py

created on 06.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import hmac
import pickle
import hashlib
import os
import sys
import uuid

from game import Game
from formatting import Color, Text, Dice


class Terminal:
    """handles terminal data"""

    def __init__(self):
        self.current_game = None
        self.clear_console()
        self.print_menu()
        self.menu_input()

    @staticmethod
    def error_handler(error):
        """handles all errors for the program

        Args:
            error (String): the error that python throws
        """
        match error:
            case "unsupported input":
                print("\n    Error: Input not supported.")
            case "already set":
                print("\n    Error: This value is already set. Enter a different number.")
            case "number not found":
                print("\n    Error: The given number was not found.")
            case "file not found":
                print("\n    Error: File 'games.bin' was not found. Please make sure this file exists in /src. ")
            case "permission error":
                print("\n    Error: This programme does not have the necessary permissions to access the file 'games.bin'."
                      "    Please make sure that the programme has full access to the file.")
            case "no saved game":
                print("\n    Error: There is no saved game.")
            case "integrity fail":
                print("\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.")
            case _:
                print("\n    Error: A unknown error occurred.")

    @staticmethod
    def clear_console():
        """clears console based on operating system"""

        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def print_menu():
        """prints main menu after program start"""

        print(f"""{Text.IMPORTANT}
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █▄─█▀▀▀█─▄█▄─▄█▄─▄███▄─▄███▄─█─▄█─▄▄─█▄─▀█▀─▄█▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄███░▄▄░▄█▄─██─▄█
    ██─█─█─█─███─███─██▀██─██▀██─▄▀██─██─██─█▄█─███─█▄█─███─▄█▀██─█▄▀─█████▀▄█▀██─██─██
    ██▄▄▄█▄▄▄██▄▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄█▄▄█▄▄▄▄█▄▄▄█▄▄▄█▄▄▄█▄▄▄█▄▄▄▄▄█▄▄▄██▄▄███▄▄▄▄▄██▄▄▄▄██
        """)

        print("""
                        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
                        █▄─█─▄█▄─▀█▄─▄█▄─▄█▄─▄▄─█▄─▄▄─█▄─▄▄─█▄─▄███
                        ██─▄▀███─█▄▀─███─███─▄████─▄████─▄█▀██─██▀█
                        █▄▄█▄▄█▄▄▄██▄▄█▄▄▄█▄▄▄███▄▄▄███▄▄▄▄▄█▄▄▄▄▄█
        """)

        print(f"""
                                    {Text.REGULAR}Start new game [S]""")
        print(f"""
                                      {Text.REGULAR}Load game [L]""")
        print(f"""
                                        {Text.IMPORTANT}Quit [Q]""")

    def menu_input(self):
        """handles inputs for main menu"""

        action = input(f"\n{Text.REGULAR}    Enter action: ")

        if action in ("s" or "S"):
            if self.check_for_game():
                overwrite_query = input(
                    """
    There is a currently a saved game.
    If you start a new game, the saved game will be lost.

    Do you want to continue? [Y/N]: """
                )
                if overwrite_query in ("y" or "Y"):
                    self.create_new_game()
                    self.play_game()
                elif overwrite_query in ("n" or "N"):
                    print("    Game creation was cancelled.")
                    self.menu_input()
                else:
                    self.error_handler("unsupported input")
                    self.menu_input()
            else:
                self.create_new_game()
                self.play_game()

        elif action in ("l" or "L"):
            self.load_game()
            if self.current_game:
                self.play_game()
            else:
                self.menu_input()
        elif action in ("q" or "Q"):
            sys.exit(0)
        else:
            self.error_handler("unsupported input")
            self.menu_input()

    def create_new_game(self):
        """creates a new game object"""

        game_id = uuid.uuid4()
        self.current_game = Game(game_id)

    def play_game(self):
        """looping through game turns and printing the winner"""

        turn = self.current_game.get_current_turn()

        while turn < 13:
            for index in range(1, 3):
                self.player_action(index, turn)
            self.save_game()
            turn += 1

        self.clear_console()
        for index in range(1, 3):
            if index == 1:
                player = self.current_game.player_1
            else:
                player = self.current_game.player_2

            print(f"{Text.PLAYER}    Player {index}:{Color.END}")
            self.show_scoreboard(player)
            print(f"{Text.SCORE}      Total:             {player.get_total_score()}{Color.END}")

        winner_id = self.current_game.get_winner()

        if winner_id == 1:
            print(f"{Text.IMPORTANT}\n        Player 1 has won!{Color.END}")
        elif winner_id == 2:
            print(f"{Text.IMPORTANT}\n        Player 2 has won!{Color.END}")
        else:
            print(f"{Text.IMPORTANT}\n          It's a draw!{Color.END}")

        self.delete_game()

    def player_action(self, player_id, turn):
        """handling the actions for one player turn

        Args:
            :param player_id: current player id (player 1 or 2)
            :param turn: current game turn
        """

        if player_id == 1:
            player = self.current_game.player_1
        else:
            player = self.current_game.player_2

        attempt = 1
        player.dice_put_aside = []

        while attempt <= 3 and len(player.dice_put_aside) != 5:
            self.clear_console()
            print(f"\n{Text.TURN}    Turn {turn + 1}{Color.END}")
            print(f"\n{Text.PLAYER}    Player {player_id} is on:{Color.END}")
            self.show_scoreboard(player)
            player.throw_dice()

            if attempt < 3:
                print(f"\n{Text.REGULAR}    You have thrown:")
                self.print_dice_symbols(player.dice_used)
                if len(player.dice_put_aside) > 0:
                    print(f"{Text.REGULAR}    The following dice are put aside:\n")
                    self.print_dice_symbols(player.dice_put_aside)
                    player.reuse_dice()
                for value in player.dice_used:
                    print(f"{Text.REGULAR}    Do you want rethrow the dice with current value {Text.SCORE + str(value) + Color.END}?")
                    action = input(f"{Text.REGULAR}    Enter action [Y/N]:\n"
                                   f"   Enter 'K' to keep all remaining dice: ")
                    if action in ("n" or "N"):
                        player.put_dice_aside(value)
                    elif action in ("k" or "K"):
                        for value2 in player.dice_used:
                            player.put_dice_aside(value2)
                        break
                attempt += 1
            else:
                for value in player.dice_used:
                    player.put_dice_aside(value)
            player.dice_put_aside.sort()

        self.clear_console()
        print(f"\n{Text.IMPORTANT}    Results {Text.TURN}Turn {turn + 1} {Text.IMPORTANT}| {Text.PLAYER}Player {player_id}")
        self.print_dice_symbols(player.dice_put_aside)
        self.show_scoreboard(player, calculate_possible_scores=True)
        self.save_round_score(player)

    @staticmethod
    def print_dice_symbols(array):
        """print dice symbols for given int array"""

        dice = []

        for element in array:
            match element:
                case 1:
                    dice.append(Dice.ONE)
                case 2:
                    dice.append(Dice.TWO)
                case 3:
                    dice.append(Dice.THREE)
                case 4:
                    dice.append(Dice.FOUR)
                case 5:
                    dice.append(Dice.FIVES)
                case 6:
                    dice.append(Dice.SIX)

        columns = [column.split('\n') for column in dice]

        lines = zip(*columns)

        max_length_of_column = [
            max([len(element) for element in column])
            for column in columns
        ]

        for parts in lines:
            padded_dice = [
                parts[i].ljust(max_length_of_column[i])
                for i in range(len(parts))
            ]
            print(''.join(padded_dice))

    @staticmethod
    def show_scoreboard(player, calculate_possible_scores=False):
        """shows results for one player

        Args:
            :param player: player object of player 1 or 2
            :param calculate_possible_scores:
        """

        keys = ["ones", "twos", "threes", "fours", "fives", "sixes", "three_of_a_kind", "four_of_a_kind",
                "full_house", "small_straight", "large_straight", "yahtzee", "chance"]

        upper = player.upper_section_score
        lower = player.lower_section_score
        scores = []
        if calculate_possible_scores:
            scores = player.get_all_possible_scores()
        else:
            for index in range(13):
                if index < 6:
                    scores.append("--" if upper[keys[index]] is None else upper[keys[index]])
                else:
                    scores.append("--" if lower[keys[index]] is None else lower[keys[index]])

        strings = ["      1) Ones:           ", "      2) Twos:           ", "      3) Threes:         ", "      4) Fours:          ",
                   "      5) Fives:          ", "      6) Sixes:          ", "      7) Three of a Kind:", "      8) Four of a Kind: ",
                   "      9) Full House:     ", "      10) Small Straight:", "      11) Large Straight:", "      12) Yahtzee:       ",
                   "      13) Chance:        "]

        print(f"{Text.REGULAR}    Your scores are:")
        print("      Upper Section:")
        for index in range(13):
            if index < 6:
                print(f""" {Text.REGULAR}{strings[index]}   {Color.BOLD + str(upper[keys[index]]) if scores[index] is None
                else Text.IMPORTANT + str(scores[index])}""")
            else:
                print(f""" {Text.REGULAR}{strings[index]}   {Color.BOLD + str(lower[keys[index]]) if scores[index] is None
                else Text.IMPORTANT + str(scores[index])}""")

            if index == 5:
                print(f"{Text.REGULAR}      Lower Section:")

    def save_round_score(self, player):
        """saves score of current round to dict

        Args:
            player (dynamic): player object of player 1 or 2
        """

        scores = player.get_all_possible_scores()
        upper = player.upper_section_score
        lower = player.lower_section_score

        score_number = input(f"\n{Text.REGULAR}    Enter the matching number to save the score: ")

        keys = ["ones", "twos", "threes", "fours", "fives", "sixes", "three_of_a_kind", "four_of_a_kind",
                "full_house", "small_straight", "large_straight", "yahtzee", "chance"]

        found = False
        for index in range(13):
            if score_number == str(index + 1):
                if index < 6:
                    upper[keys[index]] = scores[index] if upper[keys[index]] is None else (
                        self.error_handler("already set"), self.save_round_score(player))
                else:
                    lower[keys[index]] = scores[index] if lower[keys[index]] is None else (
                        self.error_handler("already set"), self.save_round_score(player))

                found = True
                break

        if not found:
            self.error_handler("number not found")
            self.save_round_score(player)

    def save_game(self):
        """pickles the current game, creates a Message Authentication code and saves everything into a binary file"""
        pickled_game = pickle.dumps(self.current_game)
        mac = hmac.new(str(self.current_game.key).encode(), pickled_game, hashlib.sha256).digest()
        game_data_b = mac + str(self.current_game.key).encode() + pickled_game
        try:
            with open("games.bin", "wb") as file:
                pickle.dump(game_data_b, file)
            print("saved")
        except FileNotFoundError:
            self.error_handler("file not found")
            self.menu_input()
        except PermissionError:
            self.error_handler("permission error")
            self.menu_input()

    def load_game(self):
        """Checks Message Authentication codes. If the codes are the same,
         the game gets loaded, otherwise it gets deleted."""

        data = self.check_for_game()
        if data:
            mac = data[16:48]
            key = data[48:52]
            game_data = data[52:(len(data) - 2)]
            mac_new = hmac.new(key, game_data, hashlib.sha256).digest()
            if hmac.compare_digest(mac, mac_new):
                print("Game was successfully loaded.")
                self.current_game = pickle.loads(game_data)
            else:
                self.error_handler("integrity fail")
                self.delete_game()
        else:
            self.error_handler("no saved game")

    def check_for_game(self):
        """ checks if a game is saved in the binary file"""
        data = None
        try:
            with open("games.bin", "rb") as file:
                data = file.read()
        except FileNotFoundError:
            self.error_handler("file not found")
        except PermissionError:
            self.error_handler("permission error")
        except EOFError:
            self.error_handler("no saved game")
        return data

    def delete_game(self):
        """ removes game save from binary file"""

        try:
            with open("games.bin", "wb") as file:
                file.truncate()
                file.close()
            print("Game was removed from save file.")
        except FileNotFoundError:
            self.error_handler("file not found")
            self.menu_input()
        except PermissionError:
            self.error_handler("permission error")
            self.menu_input()


if __name__ == "__main__":
    Terminal()

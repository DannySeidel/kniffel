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
from uuid import uuid4

from game import Game
from formatting import Color, Text, Dice


class Terminal:
    """handles terminal data"""

    def __init__(self):
        self._current_game = None
        self.__score_keys = list(Game(uuid4()).player_1.scores.keys())

    @staticmethod
    def _error_handler(error_str):
        """handles all errors for the program

        Args:
            :param error_str: the type of error represented by a string
        """

        match error_str:
            case "unsupported input":
                print("\n    Error: Input not supported.")
            case "already set":
                print("\n    Error: This value is already set. Enter a different number.")
            case "number not found":
                print("\n    Error: The given number was not found.")
            case "file not found":
                print("\n    Error: File 'games.bin' was not found. Please make sure this file exists.")
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

        while True:
            action = input(f"\n{Text.REGULAR}    Enter action: ")
            if action.upper() == "S":
                if self.__check_for_game():
                    overwrite_query = input(
                        """
        There is a currently a saved game.
        If you start a new game, the saved game will be lost.

        Do you want to continue? [Y/N]: """
                    )
                    if overwrite_query.upper() == "Y":
                        self._create_new_game()
                        self._play_game()
                    elif overwrite_query.upper() == "N":
                        print("    Game creation was cancelled.")
                    else:
                        self._error_handler("unsupported input")
                else:
                    self._create_new_game()
                    self._play_game()

            elif action.upper() == "L":
                self._load_game()
                if self._current_game:
                    self._play_game()

            elif action.upper() == "Q":
                sys.exit(0)
            else:
                self._error_handler("unsupported input")

    def _create_new_game(self):
        """creates a new game object"""

        game_id = uuid4()
        self._current_game = Game(game_id)

    def _play_game(self):
        """looping through game turns and printing the winner"""

        turn = self._current_game.get_current_turn()

        while turn < 13:
            for index in range(1, 3):
                self.__player_action(index, turn)
            self._save_game()
            turn += 1

        self.clear_console()
        for index in range(1, 3):
            if index == 1:
                player = self._current_game.player_1
            else:
                player = self._current_game.player_2

            print(f"{Text.PLAYER}    Player {index}:{Color.END}")
            self._show_scoreboard(player)
            print(f"{Text.SCORE}      Total:             {player.get_total_score()}{Color.END}")

        winner_id = self._current_game.get_winner()

        if winner_id == 1:
            print(f"{Text.IMPORTANT}\n        Player 1 has won!{Color.END}")
        elif winner_id == 2:
            print(f"{Text.IMPORTANT}\n        Player 2 has won!{Color.END}")
        else:
            print(f"{Text.IMPORTANT}\n          It's a draw!{Color.END}")

        self.__delete_game()
        # "End screen"
        input(f"{Text.REGULAR}Press Enter to return to main menu")
        self.clear_console()
        self.print_menu()

    def __player_action(self, player_id, turn):
        """handling the actions for one player turn
        Args:
            :param player_id: current player id (player 1 or 2)
            :param turn: current game turn
        """

        if player_id == 1:
            player = self._current_game.player_1
        else:
            player = self._current_game.player_2

        attempt = 1
        player.dice_put_aside = []

        while attempt <= 3 and len(player.dice_put_aside) != 5:
            self.clear_console()
            print(f"\n{Text.TURN}    Turn {turn + 1}{Color.END}")
            print(f"\n{Text.PLAYER}    Player {player_id} is on:{Color.END}")
            self._show_scoreboard(player)
            player.throw_dice()

            if attempt < 3:
                print(f"\n{Text.REGULAR}    You have thrown:")
                self._print_dice_symbols(player.dice_thrown)
                if len(player.dice_put_aside) > 0:
                    print(f"{Text.REGULAR}    The following dice are put aside:\n")
                    self._print_dice_symbols(player.dice_put_aside)
                    player.reuse_dice()
                for counter in range(len(player.dice_thrown)):
                    print(f"{Text.REGULAR}    Keep all remaining dice [K]: ")
                    print(f"    Do you want rethrow the dice with current value"
                          f" {Text.SCORE + str(player.dice_thrown[counter]) + Color.END}?")
                    action = input(f"{Text.REGULAR}    Enter action [Y/N/K]: ")

                    if action.upper() == "N":
                        player.put_dice_aside(player.dice_thrown[counter])

                    elif action.upper() == "K":
                        # Clears put_aside list to properly re-add the dice,
                        # checks all dice for rethrowing, and puts dice aside with value <= 6,
                        # if value is > 6, the dice gets rethrown
                        player.dice_put_aside.clear()
                        for value_2 in player.dice_thrown:
                            if value_2 <= 6:
                                player.put_dice_aside(value_2)
                        player.dice_thrown.clear()
                        break
                    else:
                        # increase value of dice that will be rethrown, so it can be filtered out later
                        player.dice_thrown[counter] += 6

                attempt += 1
            else:
                # puts all dice aside
                for value in player.dice_thrown:
                    player.put_dice_aside(value)
            player.dice_put_aside.sort()

        self.clear_console()
        print(f"\n{Text.IMPORTANT}    Results {Text.TURN}Turn {turn + 1} {Text.IMPORTANT}| {Text.PLAYER}Player {player_id}")
        self._print_dice_symbols(player.dice_put_aside)
        self._show_scoreboard(player, calculate_possible_scores=True)
        self._save_round_score(player)

    @staticmethod
    def _print_dice_symbols(array):
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

    def _show_scoreboard(self, player, calculate_possible_scores=False):
        """shows results for one player

        Args:
            :param player: player object of player 1 or 2
            :param calculate_possible_scores: if true possible scores of current round are calculated
        """

        saved_scores = player.scores
        possible_scores = []
        if calculate_possible_scores:
            possible_scores = player.get_all_possible_scores()
        else:
            for index in range(13):
                possible_scores.append("--" if saved_scores[self.__score_keys[index]] is None else saved_scores[self.__score_keys[index]])

        strings = ["      1) Ones:           ", "      2) Twos:           ", "      3) Threes:         ", "      4) Fours:          ",
                   "      5) Fives:          ", "      6) Sixes:          ", "      7) Three of a Kind:", "      8) Four of a Kind: ",
                   "      9) Full House:     ", "      10) Small Straight:", "      11) Large Straight:", "      12) Yahtzee:       ",
                   "      13) Chance:        "]

        print(f"{Text.REGULAR}    Your scores are:")
        print("      Upper Section:")
        for index in range(13):
            print(f""" {Text.REGULAR}{strings[index]}   {Text.SCORE + str(saved_scores[self.__score_keys[index]]) if possible_scores[index] is None
            else Text.IMPORTANT + str(possible_scores[index])}""")

            if index == 5:
                print(f"{Text.REGULAR}      Lower Section:")

    def _save_round_score(self, player):
        """saves score of current round to dict

        Args:
            :param player: player object of player 1 or 2
        """
        # TODO: fix (None,None) bug: if someone tries to set the same score twice, the score turns into (None,None)
        possible_scores = player.get_all_possible_scores()
        saved_scores = player.scores

        score_number = input(f"\n{Text.REGULAR}    Enter the matching number to save the score: ")

        found = False
        for index in range(13):
            if score_number == str(index + 1):
                saved_scores[self.__score_keys[index]] = possible_scores[index] if saved_scores[self.__score_keys[index]] is None else (
                    self._error_handler("already set"), self._save_round_score(player))

                found = True
                break

        if not found:
            self._error_handler("number not found")
            self._save_round_score(player)

    def _save_game(self):
        """pickles the current game, creates a Message Authentication code and saves everything into a binary file"""
        pickled_game = pickle.dumps(self._current_game)
        mac = hmac.new(str(self._current_game.key).encode(), pickled_game, hashlib.sha256).digest()
        game_data_b = mac + str(self._current_game.key).encode() + pickled_game
        try:
            with open("games.bin", "wb") as file:
                pickle.dump(game_data_b, file)
            print("saved")
        except FileNotFoundError:
            self._error_handler("file not found")
        except PermissionError:
            self._error_handler("permission error")

    def _load_game(self):
        """Checks Message Authentication codes.
         If the codes are the same, the game gets loaded, otherwise it gets deleted."""

        game_exists = self.__check_for_game()
        if game_exists:
            # pulls the necessary data from the "data" object
            mac = game_exists[16:48]
            key = game_exists[48:52]
            game_data = game_exists[52:(len(game_exists) - 2)]
            # creates new MAC with data read from file and compares it the the old MAC
            mac_new = hmac.new(key, game_data, hashlib.sha256).digest()
            if hmac.compare_digest(mac, mac_new):
                self._current_game = pickle.loads(game_data)
            else:
                self._error_handler("integrity fail")
                self.__delete_game()
        else:
            self._error_handler("no saved game")

    def __check_for_game(self):
        """
        checks if the file games.bin has data in it
        :return: If True: return file content
                 If False: return false
        """
        try:
            with open("games.bin", "rb") as file:
                game_data = file.read()
        except FileNotFoundError:
            self._error_handler("file not found")
        except PermissionError:
            self._error_handler("permission error")
        except EOFError:
            self._error_handler("no saved game")

        if game_data:
            return game_data

        return False

    def __delete_game(self):
        """ removes game save from binary file"""

        try:
            with open("games.bin", "wb") as file:
                file.truncate()
                file.close()
            print("Game was removed from save file.")
        except FileNotFoundError:
            self._error_handler("file not found")
        except PermissionError:
            self._error_handler("permission error")


if __name__ == "__main__":
    terminal = Terminal()
    terminal.clear_console()
    terminal.print_menu()
    terminal.menu_input()

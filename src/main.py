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

try:
    from game import Game
    from error_handler import ErrorHandler
    from formatting import Color, Text, Dice
except FileNotFoundError:
    print("Error: Core files missing. Game can't be started. Please make sure all files are in one folder")
    sys.exit(0)


class Terminal:
    """handles terminal data"""

    def __init__(self):
        self._current_game = None
        self.__score_keys = list(Game(uuid4()).player_1.scores.keys())
        self._error_handler = ErrorHandler()

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
                if self._check_for_game():
                    self._overwrite_game_query()
                else:
                    print("\n    Game was successfully created.")
                    self._create_new_game()
                    if __name__ == "__main__":
                        self._play_game()

            elif action.upper() == "L":
                self._load_game()
                if self._current_game:
                    print("\n    Game was successfully loaded.")
                    if __name__ == "__main__":
                        self._play_game()

            elif action.upper() == "Q":
                print("\n    Quitting game...")
                sys.exit(0)
            else:
                self._error_handler.input_error("unsupported input")

    def _overwrite_game_query(self):
        """
        Checks if user wants to overwrite a saved game when creating a new one
        """
        while True:
            overwrite_query = input(
                """
        There is a currently a saved game.
        If you start a new game, the saved game will be lost.

        Do you want to continue? [Y/N]: """
            )
            if overwrite_query.upper() == "Y":
                print("\n    Game was successfully created.")
                self._create_new_game()
                # prevents calling play_game when testing
                if __name__ == "__main__":
                    self._play_game()
                break
            if overwrite_query.upper() == "N":
                print("\n    Game creation was cancelled.")
                break
            self._error_handler.input_error("unsupported input")

    def _create_new_game(self):
        """creates a new game object"""

        game_id = uuid4()
        self._current_game = Game(game_id)

    def _play_game(self):
        """looping through game turns and printing the winner"""

        turn = self._current_game.get_current_turn()
        # loops through game turns
        while turn < 13:
            for index in range(1, 3):
                self.__player_action(index, turn)
            self._save_game()
            turn += 1
        self.__print_end_results()

        # End screen
        input(f"{Text.REGULAR}Enter anything to return to main menu: ")
        self.clear_console()
        self.print_menu()

    def __print_end_results(self):
        """prints final scoreboard for both players"""

        self.clear_console()
        for index in range(1, 3):
            if index == 1:
                player = self._current_game.player_1
            else:
                player = self._current_game.player_2

            print(f"{Text.PLAYER}    Player {index}:{Color.END}")
            self._show_scoreboard(player)
            print(f"{Text.SCORE}      Total:                 {player.get_total_score()}{Color.END}")
        # get winner
        winner_id = self._current_game.get_winner()

        if winner_id == 1:
            print(f"{Text.IMPORTANT}\n        Player 1 has won!{Color.END}")
        elif winner_id == 2:
            print(f"{Text.IMPORTANT}\n        Player 2 has won!{Color.END}")
        else:
            print(f"{Text.IMPORTANT}\n          It's a draw!{Color.END}")

        self._delete_game()

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

        attempt = 0
        player.dice_put_aside = []

        while attempt < 4 and len(player.dice_put_aside) != 5:
            player.throw_dice()

            if attempt < 3:
                self.clear_console()
                print(f"\n{Text.TURN}    Turn {turn + 1}{Color.END}")
                print(f"\n{Text.PLAYER}    Player {player_id} is on:{Color.END}")
                self._show_scoreboard(player)

                print(f"\n{Text.REGULAR}    You have thrown:")
                self._print_dice_symbols(player.dice_thrown)
                if len(player.dice_put_aside) > 0:
                    print(f"{Text.REGULAR}    The following dice are put aside:\n")
                    self._print_dice_symbols(player.dice_put_aside)
                    player.reuse_dice()

                self.__player_dice_input(player)

            else:
                # puts all dice aside
                for dice in player.dice_thrown:
                    player.put_dice_aside(dice)

            attempt += 1

        self.clear_console()
        player.dice_put_aside.sort()
        print(f"\n{Text.IMPORTANT}    Results {Text.TURN}Turn {turn + 1} {Text.IMPORTANT}| {Text.PLAYER}Player {player_id}")
        self._print_dice_symbols(player.dice_put_aside)
        self._show_scoreboard(player, calculate_possible_scores=True)
        # gives scoreboard number to player for saving
        while True:
            try:
                score_number = input(f"\n{Text.REGULAR}    Enter the matching number to save the score: ")
                success = player.save_round_score(int(score_number))
                if success:
                    break
            except ValueError:
                self._error_handler.input_error("invalid number")

    @staticmethod
    def __player_dice_input(player):
        action = ""
        for dice in player.dice_thrown:
            if action != "k":
                print(f"{Text.REGULAR}    Keep all remaining dice [K]")
                print(f"    Do you want rethrow the dice with current value"
                      f" {Text.SCORE + str(dice) + Color.END}?")
                print(f"{Text.REGULAR}    Other inputs are equal to [Y]")
                action = input("    Enter action [Y/N/K]: ")

            if action.upper() == "N":
                player.put_dice_aside(dice)
                action = ""

            elif action.upper() == "K":
                player.put_dice_aside(dice)
                action = "k"

            else:
                action = ""

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

    def _save_game(self):
        """pickles the current game, creates a Message Authentication code and saves everything into a binary file"""

        # pickle current game
        pickled_game = pickle.dumps(self._current_game)
        # create MAC
        mac = hmac.new(str(self._current_game.key).encode(), pickled_game, hashlib.sha256).digest()
        # combine pickled game, MAC, and game key into one binary output
        game_data_b = mac + str(self._current_game.key).encode() + pickled_game
        # save output to game file
        try:
            with open("games.bin", "wb") as file:
                pickle.dump(game_data_b, file)
            print("saved")
        except PermissionError:
            self._error_handler.file_error("permission error")

    def _load_game(self):
        """Checks Message Authentication codes.
         If the codes are the same, the game gets loaded, otherwise it gets deleted."""

        game_exists = self._check_for_game()
        if game_exists:
            # checks length of file data to prevent Errors later
            # also an integrity fail because this scenario can only happen through human tampering
            if len(game_exists) <= 55:
                self._error_handler.file_error("integrity fail")
                self._delete_game()
            else:
                # pulls the necessary data from the "data" object
                mac = game_exists[16:48]
                key = game_exists[48:52]
                game_data = game_exists[52:(len(game_exists) - 2)]

                # creates new MAC with data read from file and compares it the the old MAC
                mac_new = hmac.new(key, game_data, hashlib.sha256).digest()
                if hmac.compare_digest(mac, mac_new):
                    self._current_game = pickle.loads(game_data)
                    print("Loading success")
                else:
                    self._error_handler.file_error("integrity fail")
                    self._delete_game()
        else:
            self._error_handler.file_error("no saved game")

    def _check_for_game(self):
        """
        checks if the file games.bin has data in it
        :return: If True: return file content
                 If False: return False
        """
        game_data = False
        try:
            with open("games.bin", "rb") as file:
                game_data = file.read()
        except FileNotFoundError:
            self._error_handler.file_error("file not found")
        except PermissionError:
            self._error_handler.file_error("permission error")
        except EOFError:
            self._error_handler.file_error("no saved game")

        if game_data:
            return game_data
        return False

    def _delete_game(self):
        """ removes game save from binary file"""
        if self._check_for_game():
            try:
                with open("games.bin", "wb") as file:
                    file.truncate()
                    file.close()
                print("    Game was removed from save file.")
            except PermissionError:
                self._error_handler.file_error("permission error")


if __name__ == "__main__":
    terminal = Terminal()
    terminal.clear_console()
    terminal.print_menu()
    terminal.menu_input()

# pylint: disable=C
# pylint: disable=protected-access

import io
import sys
import unittest

from src.main import Terminal
from src.player import Player
from src.formatting import Text


class TestMain(unittest.TestCase):
    test_terminal = Terminal()

    def test_error_handler1(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("unsupported input")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: Input not supported.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler2(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("already set")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: This value is already set. Enter a different number.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler3(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("number not found")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: The given number was not found.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler4(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("file not found")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: File 'games.bin' was not found. Please make sure this file exists.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler5(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("permission error")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: This programme does not have the necessary permissions to access the file 'games.bin'." \
                       "    Please make sure that the programme has full access to the file.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler6(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("no saved game")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: There is no saved game.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler7(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("integrity fail")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler8(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._error_handler("---")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: A unknown error occurred.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_create_game(self):
        self.test_terminal._create_new_game()

        self.assertTrue(self.test_terminal.current_game)

    def test_print_menu(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.print_menu()
        sys.stdout = sys.__stdout__
        expected_str1 = f"""{Text.IMPORTANT}
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █▄─█▀▀▀█─▄█▄─▄█▄─▄███▄─▄███▄─█─▄█─▄▄─█▄─▀█▀─▄█▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄███░▄▄░▄█▄─██─▄█
    ██─█─█─█─███─███─██▀██─██▀██─▄▀██─██─██─█▄█─███─█▄█─███─▄█▀██─█▄▀─█████▀▄█▀██─██─██
    ██▄▄▄█▄▄▄██▄▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄█▄▄█▄▄▄▄█▄▄▄█▄▄▄█▄▄▄█▄▄▄█▄▄▄▄▄█▄▄▄██▄▄███▄▄▄▄▄██▄▄▄▄██
    \n"""

        expected_str2 = """
                        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
                        █▄─█─▄█▄─▀█▄─▄█▄─▄█▄─▄▄─█▄─▄▄─█▄─▄▄─█▄─▄███
                        ██─▄▀███─█▄▀─███─███─▄████─▄████─▄█▀██─██▀█
                        █▄▄█▄▄█▄▄▄██▄▄█▄▄▄█▄▄▄███▄▄▄███▄▄▄▄▄█▄▄▄▄▄█
        \n"""

        expected_str3 = f"""
                                    {Text.REGULAR}Start new game [S]\n"""

        expected_str4 = f"""
                                      {Text.REGULAR}Load game [L]\n"""

        expected_str5 = f"""
                                        {Text.IMPORTANT}Quit [Q]\n"""

        expected_output = expected_str1 + expected_str2 + expected_str3 + expected_str4 + expected_str5

        self.assertEqual(expected_output, captured_output.getvalue())

    def test_print_dice_symbols1(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._print_dice_symbols([1, 2, 3, 4, 5, 6])
        sys.stdout = sys.__stdout__
        expected_output = f"""{(Text.DICE + "       ") * 6}
    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄
    █          █    █  ▄▄      █    █ ██       █    █  ██  ██  █    █ ██    ██ █    █  ▀▀  ▀▀  █
    █    ██    █    █  ▀▀  ▄▄  █    █    ██    █    █          █    █    ██    █    █  ██  ██  █
    █          █    █      ▀▀  █    █       ██ █    █  ██  ██  █    █ ██    ██ █    █  ▄▄  ▄▄  █
    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀
                                                                                                \n"""

        self.assertEqual(expected_output, captured_output.getvalue())

    def test_show_scoreboard1(self):
        test_player = Player(1)
        test_player.dice_put_aside = [2, 3, 4, 5, 5]

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._show_scoreboard(test_player, calculate_possible_scores=True)
        sys.stdout = sys.__stdout__

        possible_scores = test_player.get_all_possible_scores()
        saved_scores = test_player.scores

        expected_str = f"{Text.REGULAR}    Your scores are:\n" \
                       "      Upper Section:\n" \
                       f""" {Text.REGULAR}      1) Ones:              {Text.SCORE + str(saved_scores['ones']) if possible_scores[0] is None
                       else Text.IMPORTANT + str(possible_scores[0])}\n"""\
                       f""" {Text.REGULAR}      2) Twos:              {Text.SCORE + str(saved_scores['twos']) if possible_scores[1] is None
                       else Text.IMPORTANT + str(possible_scores[1])}\n"""\
                       f""" {Text.REGULAR}      3) Threes:            {Text.SCORE + str(saved_scores['threes']) if possible_scores[2] is None
                       else Text.IMPORTANT + str(possible_scores[2])}\n"""\
                       f""" {Text.REGULAR}      4) Fours:             {Text.SCORE + str(saved_scores['fours']) if possible_scores[3] is None
                       else Text.IMPORTANT + str(possible_scores[3])}\n"""\
                       f""" {Text.REGULAR}      5) Fives:             {Text.SCORE + str(saved_scores['fives']) if possible_scores[4] is None
                       else Text.IMPORTANT + str(possible_scores[4])}\n"""\
                       f""" {Text.REGULAR}      6) Sixes:             {Text.SCORE + str(saved_scores['sixes']) if possible_scores[5] is None
                       else Text.IMPORTANT + str(possible_scores[5])}\n"""\
                       f"{Text.REGULAR}      Lower Section:\n"\
                       f""" {Text.REGULAR}      7) Three of a Kind:   {Text.SCORE + str(saved_scores['three_of_a_kind']) if possible_scores[6] is None
                       else Text.IMPORTANT + str(possible_scores[6])}\n"""\
                       f""" {Text.REGULAR}      8) Four of a Kind:    {Text.SCORE + str(saved_scores['four_of_a_kind']) if possible_scores[7] is None
                       else Text.IMPORTANT + str(possible_scores[7])}\n"""\
                       f""" {Text.REGULAR}      9) Full House:        {Text.SCORE + str(saved_scores['full_house']) if possible_scores[8] is None
                       else Text.IMPORTANT + str(possible_scores[8])}\n"""\
                       f""" {Text.REGULAR}      10) Small Straight:   {Text.SCORE + str(saved_scores['small_straight']) if possible_scores[9] is None
                       else Text.IMPORTANT + str(possible_scores[9])}\n"""\
                       f""" {Text.REGULAR}      11) Large Straight:   {Text.SCORE + str(saved_scores['large_straight']) if possible_scores[10] is None
                       else Text.IMPORTANT + str(possible_scores[10])}\n"""\
                       f""" {Text.REGULAR}      12) Yahtzee:          {Text.SCORE + str(saved_scores['yahtzee']) if possible_scores[11] is None
                       else Text.IMPORTANT + str(possible_scores[11])}\n"""\
                       f""" {Text.REGULAR}      13) Chance:           {Text.SCORE + str(saved_scores['chance']) if possible_scores[12] is None
                       else Text.IMPORTANT + str(possible_scores[12])}\n"""

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_show_scoreboard2(self):
        test_player = Player(2)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal._show_scoreboard(test_player)
        sys.stdout = sys.__stdout__

        possible_scores = ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        saved_scores = test_player.scores

        expected_str = f"{Text.REGULAR}    Your scores are:\n" \
                       "      Upper Section:\n" \
                       f""" {Text.REGULAR}      1) Ones:              {Text.SCORE + str(saved_scores['ones']) if possible_scores[0] is None
                       else Text.IMPORTANT + str(possible_scores[0])}\n""" \
                       f""" {Text.REGULAR}      2) Twos:              {Text.SCORE + str(saved_scores['twos']) if possible_scores[1] is None
                       else Text.IMPORTANT + str(possible_scores[1])}\n""" \
                       f""" {Text.REGULAR}      3) Threes:            {Text.SCORE + str(saved_scores['threes']) if possible_scores[2] is None
                       else Text.IMPORTANT + str(possible_scores[2])}\n""" \
                       f""" {Text.REGULAR}      4) Fours:             {Text.SCORE + str(saved_scores['fours']) if possible_scores[3] is None
                       else Text.IMPORTANT + str(possible_scores[3])}\n""" \
                       f""" {Text.REGULAR}      5) Fives:             {Text.SCORE + str(saved_scores['fives']) if possible_scores[4] is None
                       else Text.IMPORTANT + str(possible_scores[4])}\n""" \
                       f""" {Text.REGULAR}      6) Sixes:             {Text.SCORE + str(saved_scores['sixes']) if possible_scores[5] is None
                       else Text.IMPORTANT + str(possible_scores[5])}\n""" \
                       f"{Text.REGULAR}      Lower Section:\n" \
                       f""" {Text.REGULAR}      7) Three of a Kind:   {Text.SCORE + str(saved_scores['three_of_a_kind']) if possible_scores[6] is None
                       else Text.IMPORTANT + str(possible_scores[6])}\n""" \
                       f""" {Text.REGULAR}      8) Four of a Kind:    {Text.SCORE + str(saved_scores['four_of_a_kind']) if possible_scores[7] is None
                       else Text.IMPORTANT + str(possible_scores[7])}\n""" \
                       f""" {Text.REGULAR}      9) Full House:        {Text.SCORE + str(saved_scores['full_house']) if possible_scores[8] is None
                       else Text.IMPORTANT + str(possible_scores[8])}\n""" \
                       f""" {Text.REGULAR}      10) Small Straight:   {Text.SCORE + str(saved_scores['small_straight']) if possible_scores[9] is None
                       else Text.IMPORTANT + str(possible_scores[9])}\n""" \
                       f""" {Text.REGULAR}      11) Large Straight:   {Text.SCORE + str(saved_scores['large_straight']) if possible_scores[10] is None
                       else Text.IMPORTANT + str(possible_scores[10])}\n""" \
                       f""" {Text.REGULAR}      12) Yahtzee:          {Text.SCORE + str(saved_scores['yahtzee']) if possible_scores[11] is None
                       else Text.IMPORTANT + str(possible_scores[11])}\n""" \
                       f""" {Text.REGULAR}      13) Chance:           {Text.SCORE + str(saved_scores['chance']) if possible_scores[12] is None
                       else Text.IMPORTANT + str(possible_scores[12])}\n"""

        self.assertEqual(expected_str, captured_output.getvalue())

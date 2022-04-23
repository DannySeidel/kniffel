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
        self.test_terminal.error_handler("unsupported input")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: Input not supported.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler2(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("already set")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: This value is already set. Enter a different number.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler3(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("number not found")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: The given number was not found.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler4(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("file not found")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: File 'games.bin' was not found. Please make sure this file exists.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler5(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("permission error")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: This programme does not have the necessary permissions to access the file 'games.bin'." \
                       "    Please make sure that the programme has full access to the file.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler6(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("no saved game")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: There is no saved game.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler7(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("integrity fail")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler8(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.error_handler("---")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: A unknown error occurred.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

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
        self.test_terminal.print_dice_symbols([1, 2, 3, 4, 5, 6])
        sys.stdout = sys.__stdout__
        expected_output = f"""{(Text.DICE + "       ") * 6}
    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄
    █          █    █  ▄▄      █    █ ██       █    █  ██  ██  █    █ ██    ██ █    █  ▀▀  ▀▀  █
    █    ██    █    █  ▀▀  ▄▄  █    █    ██    █    █          █    █    ██    █    █  ██  ██  █
    █          █    █      ▀▀  █    █       ██ █    █  ██  ██  █    █ ██    ██ █    █  ▄▄  ▄▄  █
    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀
                                                                                                \n"""

        self.assertEqual(expected_output, captured_output.getvalue())

    def test_show_scoreboard(self):
        test_player = Player(1)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_terminal.show_scoreboard(test_player)
        sys.stdout = sys.__stdout__

        scores = ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        upper = test_player.upper_section_score
        lower = test_player.lower_section_score

        expected_str = f"{Text.REGULAR}    Your scores are:\n" \
                       "      Upper Section:\n" \
                       f""" {Text.REGULAR}      1) Ones:              {Text.SCORE + str(upper['ones']) if scores[0] is None
                       else Text.IMPORTANT + str(scores[0])}\n"""\
                       f""" {Text.REGULAR}      2) Twos:              {Text.SCORE + str(upper['twos']) if scores[1] is None
                       else Text.IMPORTANT + str(scores[1])}\n"""\
                       f""" {Text.REGULAR}      3) Threes:            {Text.SCORE + str(upper['threes']) if scores[2] is None
                       else Text.IMPORTANT + str(scores[2])}\n"""\
                       f""" {Text.REGULAR}      4) Fours:             {Text.SCORE + str(upper['fours']) if scores[3] is None
                       else Text.IMPORTANT + str(scores[3])}\n"""\
                       f""" {Text.REGULAR}      5) Fives:             {Text.SCORE + str(upper['fives']) if scores[4] is None
                       else Text.IMPORTANT + str(scores[4])}\n"""\
                       f""" {Text.REGULAR}      6) Sixes:             {Text.SCORE + str(upper['sixes']) if scores[5] is None
                       else Text.IMPORTANT + str(scores[5])}\n"""\
                       f"{Text.REGULAR}      Lower Section:\n"\
                       f""" {Text.REGULAR}      7) Three of a Kind:   {Text.SCORE + str(lower['three_of_a_kind']) if scores[6] is None
                       else Text.IMPORTANT + str(scores[6])}\n"""\
                       f""" {Text.REGULAR}      8) Four of a Kind:    {Text.SCORE + str(lower['four_of_a_kind']) if scores[7] is None
                       else Text.IMPORTANT + str(scores[7])}\n"""\
                       f""" {Text.REGULAR}      9) Full House:        {Text.SCORE + str(lower['full_house']) if scores[8] is None
                       else Text.IMPORTANT + str(scores[8])}\n"""\
                       f""" {Text.REGULAR}      10) Small Straight:   {Text.SCORE + str(lower['small_straight']) if scores[9] is None
                       else Text.IMPORTANT + str(scores[9])}\n"""\
                       f""" {Text.REGULAR}      11) Large Straight:   {Text.SCORE + str(lower['large_straight']) if scores[10] is None
                       else Text.IMPORTANT + str(scores[10])}\n"""\
                       f""" {Text.REGULAR}      12) Yahtzee:          {Text.SCORE + str(lower['yahtzee']) if scores[11] is None
                       else Text.IMPORTANT + str(scores[11])}\n"""\
                       f""" {Text.REGULAR}      13) Chance:           {Text.SCORE + str(lower['chance']) if scores[12] is None
                       else Text.IMPORTANT + str(scores[12])}\n"""

        self.assertEqual(expected_str, captured_output.getvalue())


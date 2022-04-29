# pylint: disable=C
# pylint: disable=protected-access

import io
import unittest
import os
from unittest.mock import patch

from src.main import Terminal
from src.player import Player
from src.formatting import Text


class TestMain(unittest.TestCase):

    def setUp(self):
        self.test_terminal = Terminal()

    def test_create_game(self):
        self.test_terminal._create_new_game()

        self.assertTrue(self.test_terminal._current_game)

    def test_print_menu(self):
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

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal.print_menu()
            self.assertEqual(expected_output, fake_out.getvalue())

    def test_menu_input(self):
        """
        removed "play_game" function call to simplify test
        """
        self.test_terminal._delete_game()
        expected_str_initial_input = f"{Text.REGULAR}    Enter action: \n"
        expected_str_success = "    Game was successfully created.\n"
        expected_str_quit_game = "    Quitting game...\n"
        # tests start without existing file and exit
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stdin", new=io.StringIO("s\nQ")):
                self.test_terminal.menu_input()
                fake_out.seek(0)
                actual_str = fake_out.readlines()
        self.assertEqual(expected_str_initial_input, actual_str[1])
        self.assertEqual(expected_str_success, actual_str[2])
        self.assertEqual(expected_str_initial_input, actual_str[4])
        self.assertEqual(expected_str_quit_game, actual_str[5])

        # creates a game for next round of tests
        self.test_terminal._create_new_game()
        self.test_terminal._save_game()
        expected_str_overwrite_game_query = """        There is a currently a saved game.
        If you start a new game, the saved game will be lost.

        Do you want to continue? [Y/N]: \n"""
        expected_str_cancel = "    Game creation was cancelled.\n"
        expected_str_error = "    Error: Input not supported.\n"
        expected_str_load_success = "    Game was successfully loaded.\n"

        # tests options if there is a saved game
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stdin", new=io.StringIO("s\nN\ns\nabcd\ny\nl\nabcd\nq")):
                self.test_terminal.menu_input()
                fake_out.seek(0)
        actual_str = fake_out.readlines()
        self.assertEqual(expected_str_overwrite_game_query, actual_str[2]+actual_str[3]+actual_str[4]+actual_str[5])
        self.assertEqual(expected_str_cancel, actual_str[6])
        self.assertEqual(expected_str_error, actual_str[13])
        self.assertEqual(expected_str_success, actual_str[19])
        self.assertEqual(expected_str_load_success, actual_str[23])
        self.assertEqual(expected_str_error, actual_str[26])

    def test_print_dice_symbols1(self):
        expected_output = f"""{(Text.DICE + "       ") * 6}
    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄    ▄▀▀▀▀▀▀▀▀▀▀▄
    █          █    █  ▄▄      █    █ ██       █    █  ██  ██  █    █ ██    ██ █    █  ▀▀  ▀▀  █
    █    ██    █    █  ▀▀  ▄▄  █    █    ██    █    █          █    █    ██    █    █  ██  ██  █
    █          █    █      ▀▀  █    █       ██ █    █  ██  ██  █    █ ██    ██ █    █  ▄▄  ▄▄  █
    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀    ▀▄▄▄▄▄▄▄▄▄▄▀
                                                                                                \n"""

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._print_dice_symbols([1, 2, 3, 4, 5, 6])

        self.assertEqual(expected_output, fake_out.getvalue())

    def test_show_scoreboard1(self):
        test_player = Player(1)
        test_player.dice_put_aside = [2, 3, 4, 5, 5]

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

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._show_scoreboard(test_player, calculate_possible_scores=True)
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_show_scoreboard2(self):
        test_player = Player(2)

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

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._show_scoreboard(test_player)
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_save_game(self):

        # creates test binary file
        with open("games.bin", "wb"):
            pass

        # creates new game that can be saved
        self.test_terminal._create_new_game()
        expected_str = "saved\n"

        # tests correct saving procedure
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._save_game()
            self.assertEqual(expected_str, fake_out.getvalue())
        self.test_terminal._delete_game()

    def test_check_for_game(self):

        # creates test binary file
        with open("games.bin", "wb"):
            pass

        # tests empty file handling
        expected_value_empty_file = False
        actual_value = self.test_terminal._check_for_game()
        self.assertEqual(expected_value_empty_file, actual_value)

        # sets up test for the correct procedure
        self.test_terminal._create_new_game()
        self.test_terminal._save_game()
        with open("games.bin", "rb") as file:
            expected_value_success = file.read()

        # tests correct game checking procedure
        actual_value_correct = self.test_terminal._check_for_game()
        self.assertEqual(expected_value_success, actual_value_correct)

        # removes file to check "file not found" handling
        os.remove("games.bin")

        # tests "file not found" handling
        expected_value_fnf = "\n    Error: File 'games.bin' was not found. Please make sure this file exists.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._check_for_game()
            self.assertEqual(expected_value_fnf, fake_out.getvalue())

    def test_load_game(self):
        # creates test binary file
        with open("games.bin", "wb"):
            pass

        # tests empty file handling
        expected_str_empty_file = "\n    Error: There is no saved game.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._load_game()
            self.assertEqual(expected_str_empty_file, fake_out.getvalue())

        # sets up test for too short file length
        expected_str_integrity_fail = "\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.\n" \
                                      "    Game was removed from save file.\n"

        with open("games.bin", "wb") as file:
            file.write("Random String".encode())

        # tests too short file length
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._load_game()
            self.assertEqual(expected_str_integrity_fail, fake_out.getvalue())
        self.test_terminal._delete_game()

        # sets up test for successful loading
        self.test_terminal._create_new_game()
        self.test_terminal._save_game()
        expected_str_success = "Loading success\n"

        # tests successful loading
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._load_game()
            self.assertEqual(expected_str_success, fake_out.getvalue())

        # sets up test for failed MAC comparison
        with open("games.bin", "rb") as file:
            content = file.read()
        content_changed = content + "Random string".encode()
        with open("games.bin", "wb") as file2:
            file2.write(content_changed)

        # tests failed MAC comparison
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._load_game()
            self.assertEqual(expected_str_integrity_fail, fake_out.getvalue())
        self.test_terminal._delete_game()

    def test_delete_game(self):
        with open("games.bin", "wb"):
            pass
        # sets up test for successful deleting
        self.test_terminal._create_new_game()
        self.test_terminal._save_game()
        expected_str_success = "    Game was removed from save file.\n"

        # tests sucessful deleting
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._delete_game()
            self.assertEqual(expected_str_success, fake_out.getvalue())

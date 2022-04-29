# pylint: disable=C
# pylint: disable=protected-access

import io
import unittest
import os
from unittest.mock import patch

from src.main import Terminal
from src.player import Player
from src.formatting import Color, Text


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
        # removed "play_game" function call to simplify test
        self.test_terminal._delete_game()
        expected_str_initial_input = f"{Text.REGULAR}    Enter action: \n"
        expected_str_success = "    Game was successfully created.\n"
        expected_str_quit_game = "    Quitting game...\n"

        # tests start without existing file and exit
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stdin", new=io.StringIO("s\nQ")):
                with self.assertRaises(SystemExit) as system_shutdown:
                    self.test_terminal.menu_input()
                fake_out.seek(0)
                actual_str = fake_out.readlines()
        self.assertEqual(expected_str_initial_input, actual_str[1])
        self.assertEqual(expected_str_success, actual_str[4])
        self.assertEqual(expected_str_initial_input, actual_str[6])
        self.assertEqual(expected_str_quit_game, actual_str[7])
        self.assertEqual(0, system_shutdown.exception.code)

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
                with self.assertRaises(SystemExit):
                    self.test_terminal.menu_input()
                fake_out.seek(0)
                actual_str = fake_out.readlines()
        self.assertEqual(expected_str_overwrite_game_query, actual_str[2]+actual_str[3]+actual_str[4]+actual_str[5])
        self.assertEqual(expected_str_cancel, actual_str[6])
        self.assertEqual(expected_str_error, actual_str[13])
        self.assertEqual(expected_str_success, actual_str[19])
        self.assertEqual(expected_str_load_success, actual_str[23])
        self.assertEqual(expected_str_error, actual_str[26])

    def test_play_game(self):
        # sets up a new game
        self.test_terminal._create_new_game()

        # tests game procedure
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stdin", new=io.StringIO("y\ny\nk\nn\ny\nk\n"
            "y\nk\n1\nn\nn\nn\ny\ny\ny\ny\nk\nn\nk\n1.2\n1\nk\n2\nk\n2\nk\n3\n"
            "k\n3\nk\n4\nk\n4\nk\n5\nk\n5\nk\n6\nk\n6\nk\n7\nk\n7\nk\n8\n"
            "k\n8\nk\n9\nk\n9\nk\n10\nk\n10\nk\n11\nk\n11\nk\n12\nk\n12\n"
            "k\n13\nk\n13\nfinish")):
                self.test_terminal._play_game()
                fake_out.seek(0)
                actual_str = fake_out.readlines()

        exp_str_t1 = f"{Text.TURN}    Turn 1{Color.END}\n"
        exp_str_t2 = f"{Text.TURN}    Turn 2{Color.END}\n"
        exp_str_t3 = f"{Text.TURN}    Turn 3{Color.END}\n"
        exp_str_t4 = f"{Text.TURN}    Turn 4{Color.END}\n"
        exp_str_t5 = f"{Text.TURN}    Turn 5{Color.END}\n"
        exp_str_t6 = f"{Text.TURN}    Turn 6{Color.END}\n"
        exp_str_t7 = f"{Text.TURN}    Turn 7{Color.END}\n"
        exp_str_t8 = f"{Text.TURN}    Turn 8{Color.END}\n"
        exp_str_t9 = f"{Text.TURN}    Turn 9{Color.END}\n"
        exp_str_t10 = f"{Text.TURN}    Turn 10{Color.END}\n"
        exp_str_t11 = f"{Text.TURN}    Turn 11{Color.END}\n"
        exp_str_t12 = f"{Text.TURN}    Turn 12{Color.END}\n"
        exp_str_t13 = f"{Text.TURN}    Turn 13{Color.END}\n"

        exp_str_p1 = f"{Text.PLAYER}    Player 1 is on:{Color.END}\n"
        exp_str_p2 = f"{Text.PLAYER}    Player 2 is on:{Color.END}\n"

        exp_str_you_have_thrown = f"{Text.REGULAR}    You have thrown:\n"
        exp_str_you_put_aside = f"{Text.REGULAR}    The following dice are put aside:\n"

        exp_str_t1_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 1 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t2_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 2 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t3_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 3 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t4_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 4 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t5_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 5 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t6_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 6 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t7_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 7 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t8_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 8 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t9_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 9 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t10_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 10 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t11_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 11 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t12_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 12 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t13_p1 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 13 {Text.IMPORTANT}| {Text.PLAYER}Player 1\n"
        exp_str_t1_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 1 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t2_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 2 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t3_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 3 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t4_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 4 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t5_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 5 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t6_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 6 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t7_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 7 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t8_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 8 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t9_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 9 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t10_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 10 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t11_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 11 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t12_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 12 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"
        exp_str_t13_p2 = f"{Text.IMPORTANT}    Results {Text.TURN}Turn 13 {Text.IMPORTANT}| {Text.PLAYER}Player 2\n"

        exp_str_enter_number_for_score = f"{Text.REGULAR}    Enter the matching number to save the score: \n"
        exp_str_error_inp_number = "    Error: Please choose a number between 1 and 13.\n"
        exp_str_other_inputs_are_y = f"{Text.REGULAR}    Other inputs are equal to [Y]\n"
        exp_str_keep_all_dice = f"{Text.REGULAR}    Keep all remaining dice [K]\n"
        exp_str_enter_action = "    Enter action [Y/N/K]: \n"
        exp_str_enter_keep_all = f"    Enter action [Y/N/K]: {Text.REGULAR}    Keep all remaining dice [K]\n"

        exp_str_dice_input_1 = f"    Do you want rethrow the dice with current value {Text.SCORE}1{Color.END}?\n"
        exp_str_dice_input_2 = f"    Do you want rethrow the dice with current value {Text.SCORE}2{Color.END}?\n"
        exp_str_dice_input_3 = f"    Do you want rethrow the dice with current value {Text.SCORE}3{Color.END}?\n"
        exp_str_dice_input_4 = f"    Do you want rethrow the dice with current value {Text.SCORE}4{Color.END}?\n"
        exp_str_dice_input_5 = f"    Do you want rethrow the dice with current value {Text.SCORE}5{Color.END}?\n"

        exp_str_player_1_total_p = f"{Text.PLAYER}    Player 1:{Color.END}\n"
        exp_str_players_total_t = f"{Text.SCORE}      Total:                 101{Color.END}\n"
        exp_str_player_2_total_p = f"{Text.PLAYER}    Player 2:{Color.END}\n"
        exp_str_draw = f"          It's a draw!{Color.END}\n"
        exp_str_return_input = f"{Text.REGULAR}Enter anything to return to main menu: {Text.IMPORTANT}\n"

        self.assertEqual(exp_str_t1, actual_str[1])
        self.assertEqual(exp_str_p1, actual_str[3])
        self.assertEqual(exp_str_you_have_thrown, actual_str[21])
        self.assertEqual(exp_str_keep_all_dice, actual_str[29])
        self.assertEqual(exp_str_dice_input_1, actual_str[30])
        self.assertEqual(exp_str_other_inputs_are_y, actual_str[31])
        self.assertEqual(exp_str_enter_keep_all, actual_str[32])
        self.assertEqual(exp_str_dice_input_2, actual_str[33])
        self.assertEqual(exp_str_dice_input_3, actual_str[36])
        self.assertEqual(exp_str_enter_action, actual_str[38])
        self.assertEqual(exp_str_you_put_aside, actual_str[67])

        self.assertEqual(exp_str_enter_number_for_score, actual_str[155])
        self.assertEqual(exp_str_p2, actual_str[158])
        self.assertEqual(exp_str_dice_input_4, actual_str[194])
        self.assertEqual(exp_str_dice_input_5, actual_str[197])

        self.assertEqual(exp_str_error_inp_number, actual_str[317])
        self.assertEqual(exp_str_t2, actual_str[321])
        self.assertEqual(exp_str_t3, actual_str[438])
        self.assertEqual(exp_str_t4, actual_str[555])
        self.assertEqual(exp_str_t5, actual_str[672])
        self.assertEqual(exp_str_t6, actual_str[789])
        self.assertEqual(exp_str_t7, actual_str[906])
        self.assertEqual(exp_str_t8, actual_str[1023])
        self.assertEqual(exp_str_t9, actual_str[1140])
        self.assertEqual(exp_str_t10, actual_str[1257])
        self.assertEqual(exp_str_t11, actual_str[1374])
        self.assertEqual(exp_str_t12, actual_str[1491])
        self.assertEqual(exp_str_t13, actual_str[1608])

        self.assertEqual(exp_str_t1_p1, actual_str[130])
        self.assertEqual(exp_str_t2_p1, actual_str[353])
        self.assertEqual(exp_str_t3_p1, actual_str[470])
        self.assertEqual(exp_str_t4_p1, actual_str[587])
        self.assertEqual(exp_str_t5_p1, actual_str[704])
        self.assertEqual(exp_str_t6_p1, actual_str[821])
        self.assertEqual(exp_str_t7_p1, actual_str[938])
        self.assertEqual(exp_str_t8_p1, actual_str[1055])
        self.assertEqual(exp_str_t9_p1, actual_str[1172])
        self.assertEqual(exp_str_t10_p1, actual_str[1289])
        self.assertEqual(exp_str_t11_p1, actual_str[1406])
        self.assertEqual(exp_str_t12_p1, actual_str[1523])
        self.assertEqual(exp_str_t13_p1, actual_str[1640])

        self.assertEqual(exp_str_t1_p2, actual_str[291])
        self.assertEqual(exp_str_t2_p2, actual_str[411])
        self.assertEqual(exp_str_t3_p2, actual_str[528])
        self.assertEqual(exp_str_t4_p2, actual_str[645])
        self.assertEqual(exp_str_t5_p2, actual_str[762])
        self.assertEqual(exp_str_t6_p2, actual_str[879])
        self.assertEqual(exp_str_t7_p2, actual_str[996])
        self.assertEqual(exp_str_t8_p2, actual_str[1113])
        self.assertEqual(exp_str_t9_p2, actual_str[1230])
        self.assertEqual(exp_str_t10_p2, actual_str[1347])
        self.assertEqual(exp_str_t11_p2, actual_str[1464])
        self.assertEqual(exp_str_t12_p2, actual_str[1581])
        self.assertEqual(exp_str_t13_p2, actual_str[1698])

        self.assertEqual(exp_str_player_1_total_p, actual_str[1724])
        self.assertEqual(exp_str_player_2_total_p, actual_str[1742])
        self.assertEqual(exp_str_players_total_t, actual_str[1741])
        self.assertEqual(exp_str_players_total_t, actual_str[1759])
        self.assertEqual(exp_str_draw, actual_str[1761])
        self.assertEqual(exp_str_return_input, actual_str[1763])

    def test_print_end_results1(self):

        expected_str_winner = f"        Player 1 has won!{Color.END}\n"

        # sets up test for player 1 winning
        self.test_terminal._create_new_game()
        self.test_terminal._current_game.player_1.scores = {x: 6 for x in self.test_terminal._current_game.player_1.scores}
        self.test_terminal._current_game.player_2.scores = {x: 1 for x in self.test_terminal._current_game.player_2.scores}

        # tests player 1 winning
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._print_end_results()
            fake_out.seek(0)
            actual_str = fake_out.readlines()
        self.assertEqual(expected_str_winner, actual_str[37])
        self.test_terminal._delete_game()

    def test_print_end_results2(self):

        expected_str_winner = f"        Player 2 has won!{Color.END}\n"

        # sets up test for player 2 winning
        self.test_terminal._create_new_game()
        self.test_terminal._current_game.player_1.scores = {x: 1 for x in self.test_terminal._current_game.player_1.scores}
        self.test_terminal._current_game.player_2.scores = {x: 6 for x in self.test_terminal._current_game.player_2.scores}

        # tests player 2 winning
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_terminal._print_end_results()
            fake_out.seek(0)
            actual_str = fake_out.readlines()
        self.assertEqual(expected_str_winner, actual_str[37])
        self.test_terminal._delete_game()

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

    def tearDown(self):
        try:
            os.remove("games.bin")
        except FileNotFoundError:
            pass

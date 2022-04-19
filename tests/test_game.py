# pylint: disable=C
# pylint: disable=protected-access

import unittest
import uuid
from src.game import Game


class TestGame(unittest.TestCase):
    test_game = Game(uuid.uuid4())

    def test_get_current_turn(self):
        self.test_game.player_1.upper_section_score["ones"] = 3
        self.test_game.player_1.upper_section_score["twos"] = 4
        self.test_game.player_1.upper_section_score["threes"] = None
        self.test_game.player_1.upper_section_score["fours"] = 12
        self.test_game.player_1.upper_section_score["fives"] = None
        self.test_game.player_1.upper_section_score["sixes"] = 18

        self.test_game.player_1.lower_section_score["three_of_a_kind"] = 12
        self.test_game.player_1.lower_section_score["four_of_a_kind"] = None
        self.test_game.player_1.lower_section_score["full_house"] = 25
        self.test_game.player_1.lower_section_score["small_straight"] = None
        self.test_game.player_1.lower_section_score["large_straight"] = 40
        self.test_game.player_1.lower_section_score["yahtzee"] = None
        self.test_game.player_1.lower_section_score["chance"] = 23

        expected_value = 8

        self.assertEqual(expected_value, self.test_game.get_current_turn())

    def test_get_winner(self):
        self.test_game.player_1.upper_section_score["ones"] = 5
        self.test_game.player_1.upper_section_score["twos"] = 10
        self.test_game.player_1.upper_section_score["threes"] = 9
        self.test_game.player_1.upper_section_score["fours"] = 12
        self.test_game.player_1.upper_section_score["fives"] = 10
        self.test_game.player_1.upper_section_score["sixes"] = 18

        self.test_game.player_1.lower_section_score["three_of_a_kind"] = 12
        self.test_game.player_1.lower_section_score["four_of_a_kind"] = 8
        self.test_game.player_1.lower_section_score["full_house"] = 25
        self.test_game.player_1.lower_section_score["small_straight"] = 30
        self.test_game.player_1.lower_section_score["large_straight"] = 40
        self.test_game.player_1.lower_section_score["yahtzee"] = 50
        self.test_game.player_1.lower_section_score["chance"] = 19

        self.test_game.player_2.upper_section_score["ones"] = 5
        self.test_game.player_2.upper_section_score["twos"] = 10
        self.test_game.player_2.upper_section_score["threes"] = 9
        self.test_game.player_2.upper_section_score["fours"] = 12
        self.test_game.player_2.upper_section_score["fives"] = 15
        self.test_game.player_2.upper_section_score["sixes"] = 12

        self.test_game.player_2.lower_section_score["three_of_a_kind"] = 9
        self.test_game.player_2.lower_section_score["four_of_a_kind"] = 12
        self.test_game.player_2.lower_section_score["full_house"] = 25
        self.test_game.player_2.lower_section_score["small_straight"] = 30
        self.test_game.player_2.lower_section_score["large_straight"] = 40
        self.test_game.player_2.lower_section_score["yahtzee"] = 50
        self.test_game.player_2.lower_section_score["chance"] = 16
        expected_value = 1

        self.assertEqual(expected_value, self.test_game.get_winner())

        self.test_game.player_2.lower_section_score["chance"] = 21
        expected_value = 2

        self.assertEqual(expected_value, self.test_game.get_winner())

        self.test_game.player_2.lower_section_score["chance"] = 19
        expected_value = 0

        self.assertEqual(expected_value, self.test_game.get_winner())




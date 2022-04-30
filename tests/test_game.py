# pylint: disable=C
# pylint: disable=protected-access

import unittest
from src.game import Game


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.test_game = Game()

    def test_get_current_turn(self):

        # Sets up Test for getting current game turn
        self.test_game.player_1.scores["ones"] = 3
        self.test_game.player_1.scores["twos"] = 4
        self.test_game.player_1.scores["threes"] = None
        self.test_game.player_1.scores["fours"] = 12
        self.test_game.player_1.scores["fives"] = None
        self.test_game.player_1.scores["sixes"] = 18

        self.test_game.player_1.scores["three_of_a_kind"] = 12
        self.test_game.player_1.scores["four_of_a_kind"] = None
        self.test_game.player_1.scores["full_house"] = 25
        self.test_game.player_1.scores["small_straight"] = None
        self.test_game.player_1.scores["large_straight"] = 40
        self.test_game.player_1.scores["yahtzee"] = None
        self.test_game.player_1.scores["chance"] = 23

        expected_value = 8

        # Tests if current game turn is correctly calculated
        self.assertEqual(expected_value, self.test_game.get_current_turn())

    def test_get_winner(self):

        # Sets up test for calculating the winner
        self.test_game.player_1.scores["ones"] = 5
        self.test_game.player_1.scores["twos"] = 10
        self.test_game.player_1.scores["threes"] = 9
        self.test_game.player_1.scores["fours"] = 12
        self.test_game.player_1.scores["fives"] = 10
        self.test_game.player_1.scores["sixes"] = 18

        self.test_game.player_1.scores["three_of_a_kind"] = 12
        self.test_game.player_1.scores["four_of_a_kind"] = 8
        self.test_game.player_1.scores["full_house"] = 25
        self.test_game.player_1.scores["small_straight"] = 30
        self.test_game.player_1.scores["large_straight"] = 40
        self.test_game.player_1.scores["yahtzee"] = 50
        self.test_game.player_1.scores["chance"] = 19

        self.test_game.player_2.scores["ones"] = 5
        self.test_game.player_2.scores["twos"] = 10
        self.test_game.player_2.scores["threes"] = 9
        self.test_game.player_2.scores["fours"] = 12
        self.test_game.player_2.scores["fives"] = 15
        self.test_game.player_2.scores["sixes"] = 12

        self.test_game.player_2.scores["three_of_a_kind"] = 9
        self.test_game.player_2.scores["four_of_a_kind"] = 12
        self.test_game.player_2.scores["full_house"] = 25
        self.test_game.player_2.scores["small_straight"] = 30
        self.test_game.player_2.scores["large_straight"] = 40
        self.test_game.player_2.scores["yahtzee"] = 50
        self.test_game.player_2.scores["chance"] = 16
        expected_value = 1

        # Tests Player 1 winning
        self.assertEqual(expected_value, self.test_game.get_winner())

        self.test_game.player_2.scores["chance"] = 21
        expected_value = 2

        # Tests Player 2 winning
        self.assertEqual(expected_value, self.test_game.get_winner())

        self.test_game.player_2.scores["chance"] = 19
        expected_value = 0

        # Tests a draw
        self.assertEqual(expected_value, self.test_game.get_winner())

        # Tests if bonus points are given correctly
        expected_value = sum(self.test_game.player_2.scores.values()) + 35
        actual_value = self.test_game.player_2.get_total_score()

        self.assertEqual(expected_value, actual_value)

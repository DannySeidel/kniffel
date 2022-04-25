# pylint: disable=C
# pylint: disable=protected-access

from unittest import TestCase
from src.player import Player


class TestPlayer(TestCase):
    test_player = Player(1)

    def test_throw_dice(self):
        self.test_player.dice_put_aside = [3, 3]
        expected_value = 3

        self.test_player.throw_dice()
        self.assertEqual(expected_value, len(self.test_player.dice_thrown))
        self.assertTrue(self.test_player.dice_thrown[0] <= self.test_player.dice_thrown[1])
        self.assertTrue(self.test_player.dice_thrown[1] <= self.test_player.dice_thrown[2])

    def test_get_all_possible_scores1(self):
        self.test_player.dice_put_aside = [1, 2, 3, 4, 5]
        print(self.test_player.get_all_possible_scores())
        expected_value = [1, 2, 3, 4, 5, 0, 0, 0, 0, 30, 40, 0, 15]

        self.assertEqual(expected_value, self.test_player.get_all_possible_scores())

    def test_get_all_possible_scores2(self):
        self.test_player.dice_put_aside = [2, 3, 4, 5, 6]
        print(self.test_player.get_all_possible_scores())
        expected_value = [0, 2, 3, 4, 5, 6, 0, 0, 0, 30, 40, 0, 20]

        self.assertEqual(expected_value, self.test_player.get_all_possible_scores())

    def test_get_all_possible_scores3(self):
        self.test_player.dice_put_aside = [2, 2, 4, 4, 4]
        print(self.test_player.get_all_possible_scores())
        expected_value = [0, 4, 0, 12, 0, 0, 16, 0, 25, 0, 0, 0, 16]

        self.assertEqual(expected_value, self.test_player.get_all_possible_scores())

    def test_get_all_possible_scores4(self):
        self.test_player.dice_put_aside = [3, 3, 4, 5, 6]
        print(self.test_player.get_all_possible_scores())
        expected_value = [0, 0, 6, 4, 5, 6, 0, 0, 0, 30, 0, 0, 21]

        self.assertEqual(expected_value, self.test_player.get_all_possible_scores())

    def test_get_all_possible_scores5(self):
        self.test_player.dice_put_aside = [3, 3, 3, 3, 3]
        print(self.test_player.get_all_possible_scores())
        expected_value = [0, 0, 15, 0, 0, 0, 15, 15, 0, 0, 0, 50, 15]

        self.assertEqual(expected_value, self.test_player.get_all_possible_scores())

    def test_put_dice_aside(self):
        self.test_player.dice_put_aside = [2, 4, 5]
        expected_value = [2, 4, 5, 3]

        self.test_player.put_dice_aside(3)
        self.assertEqual(expected_value, self.test_player.dice_put_aside)

    def test_reuse_dice(self):
        self.test_player.dice_thrown = [1, 4]
        self.test_player.dice_put_aside = [1, 3, 6]

        expected_value1 = [1, 4, 1, 3, 6]
        expected_value2 = []

        self.test_player.reuse_dice()
        self.assertEqual(expected_value1, self.test_player.dice_thrown)
        self.assertEqual(expected_value2, self.test_player.dice_put_aside)

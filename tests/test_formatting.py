# pylint: disable=C
# pylint: disable=protected-access

import unittest
from src.formatting import Color, Text, Dice


class TestMain(unittest.TestCase):
    def test_Color(self):
        self.assertEqual('\033[95m', Color.PURPLE)
        self.assertEqual('\033[96m', Color.CYAN)
        self.assertEqual('\033[94m', Color.BLUE)
        self.assertEqual('\033[92m', Color.GREEN)
        self.assertEqual('\033[93m', Color.YELLOW)
        self.assertEqual('\033[91m', Color.RED)
        self.assertEqual('\033[1m', Color.BOLD)
        self.assertEqual('\033[0m', Color.END)

    def test_Text(self):
        self.assertEqual(Color.BOLD + Color.RED, Text.IMPORTANT)
        self.assertEqual(Color.BOLD + Color.BLUE, Text.REGULAR)
        self.assertEqual(Color.BOLD + Color.PURPLE, Text.TURN)
        self.assertEqual(Color.BOLD + Color.CYAN, Text.PLAYER)
        self.assertEqual(Color.BOLD + Color.GREEN, Text.DICE)
        self.assertEqual(Color.BOLD + Color.YELLOW, Text.SCORE)

    def test_Dice(self):
        self.assertEqual(f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █          █
    █    ██    █
    █          █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """, Dice.ONE)

        self.assertEqual(f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █  ▄▄      █
    █  ▀▀  ▄▄  █
    █      ▀▀  █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """, Dice.TWO)

        self.assertEqual(f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █ ██       █
    █    ██    █
    █       ██ █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """, Dice.THREE)

        self.assertEqual(f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █  ██  ██  █
    █          █
    █  ██  ██  █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """, Dice.FOUR)

        self.assertEqual(f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █ ██    ██ █
    █    ██    █
    █ ██    ██ █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """, Dice.FIVES)

        self.assertEqual(f"""{Text.DICE}
    ▄▀▀▀▀▀▀▀▀▀▀▄
    █  ▀▀  ▀▀  █
    █  ██  ██  █
    █  ▄▄  ▄▄  █
    ▀▄▄▄▄▄▄▄▄▄▄▀
    """, Dice.SIX)

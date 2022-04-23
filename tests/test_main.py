# pylint: disable=C
# pylint: disable=protected-access

import io
import sys
import unittest

from src.main import Terminal
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



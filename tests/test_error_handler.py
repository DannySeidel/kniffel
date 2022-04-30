# pylint: disable=C
# pylint: disable=protected-access

import unittest
import sys
import io
from unittest.mock import patch

from src.error_handler import ErrorHandler


class TestErrorHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.test_error_handler = ErrorHandler()

    def test_error_handler1(self):

        # Tests wrong input error
        expected_str = "\n    Error: Input not supported.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.input_error("unsupported input")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler2(self):

        # Tests value already set error
        expected_str = "\n    Error: This value is already set. Enter a different number.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.input_error("already set")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler3(self):

        # Tests number not found error
        expected_str = "\n    Error: The given number was not found.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.input_error("number not found")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler4(self):

        # Tests invalid number error
        expected_str = "\n    Error: Please choose a number between 1 and 13.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.input_error("invalid number")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler5(self):

        # Tests FileNotFound error
        expected_str = "\n    Error: File 'games.bin' was not found. Please make sure this file exists.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.file_error("file not found")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler6(self):

        # Tests PermissonError
        expected_str = "\n    Error: This programme does not have the necessary permissions to access the file 'games.bin'." \
                       "    Please make sure that the programme has full access to the file.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.file_error("permission error")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler7(self):

        # Tests no saved game error
        expected_str = "\n    Error: There is no saved game.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.file_error("no saved game")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler8(self):

        # Tests integrity fail error
        expected_str = "\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.file_error("integrity fail")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler9(self):

        # Tests unknown file error
        expected_str = "\n    Error: A unknown error occurred.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.file_error("---")
            self.assertEqual(expected_str, fake_out.getvalue())

    def test_error_handler10(self):

        # Tests unknown input error
        expected_str = "\n    Error: A unknown error occurred.\n"
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.test_error_handler.input_error("---")
            self.assertEqual(expected_str, fake_out.getvalue())

# pylint: disable=C
# pylint: disable=protected-access

import unittest
import sys
import io

from src.error_handler import ErrorHandler


class TestErrorHandler(unittest.TestCase):
    test_error_handler = ErrorHandler()

    def test_error_handler1(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.input_error("unsupported input")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: Input not supported.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler2(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.input_error("already set")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: This value is already set. Enter a different number.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler3(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.input_error("number not found")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: The given number was not found.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler4(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.file_error("file not found")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: File 'games.bin' was not found. Please make sure this file exists.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler5(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.file_error("permission error")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: This programme does not have the necessary permissions to access the file 'games.bin'." \
                       "    Please make sure that the programme has full access to the file.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler6(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.file_error("no saved game")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: There is no saved game.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler7(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.file_error("integrity fail")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

    def test_error_handler8(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.test_error_handler.file_error("---")
        sys.stdout = sys.__stdout__
        expected_str = "\n    Error: A unknown error occurred.\n"

        self.assertEqual(expected_str, captured_output.getvalue())

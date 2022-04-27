"""
kniffel
error_handler.py

created on 24.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""


class ErrorHandler:
    """
    handling possible errors and throwing corresponding errortext in terminal
    """

    @staticmethod
    def input_error(error_str):
        """handles all input related errors for the program

        Args:
            :param error_str: the type of input error represented by a string
        """

        match error_str:
            case "unsupported input":
                print("\n    Error: Input not supported.")
            case "already set":
                print("\n    Error: This value is already set. Enter a different number.")
            case "number not found":
                print("\n    Error: The given number was not found.")
            case _:
                print("\n    Error: A unknown error occurred.")

    @staticmethod
    def file_error(error_str):
        """handles all file related errors for the program

        Args:
            :param error_str: the type of file error represented by a string
        """

        match error_str:
            case "file not found":
                print("\n    Error: File 'games.bin' was not found. Please make sure this file exists.")
            case "permission error":
                print("\n    Error: This programme does not have the necessary permissions to access the file 'games.bin'."
                      "    Please make sure that the programme has full access to the file.")
            case "no saved game":
                print("\n    Error: There is no saved game.")
            case "integrity fail":
                print("\n    Error: The game save file has been tampered with. The game is not recoverable and has to be deleted.")
            case _:
                print("\n    Error: A unknown error occurred.")

"""
kniffel
game.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

from random import randint
from player import Player


class Game:
    """handles game data and current game state"""

    def __init__(self, uuid, error_handling_class):
        self._uuid = uuid
        self.key = randint(1000, 9999)
        self.player_1 = Player(1, error_handling_class)
        self.player_2 = Player(2, error_handling_class)
        self.__error_handler = error_handling_class

    def get_current_turn(self) -> int:
        """returns the number of the current turn

        Returns:
            int: which turn is currently active
        """

        turn = 0

        for value in self.player_1.scores.values():
            if value is not None:
                turn += 1

        return turn

    def get_winner(self) -> int:
        """returns winner of game / returns 0 if game is a draw

        Returns:
            int: id/number of the winner
        """

        player_1_score = self.player_1.get_total_score()
        player_2_score = self.player_2.get_total_score()

        if player_1_score > player_2_score:
            return 1
        if player_1_score < player_2_score:
            return 2

        return 0

"""
kniffel
game.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

from src import player


class Game:
    """handles game data and current game state"""

    def __init__(self, uuid):
        # TODO: add randomly generated encryption key
        self.uuid = uuid
        self.player_1 = player.Player(1)
        self.player_2 = player.Player(2)

    def get_current_turn(self) -> int:
        """returns the number of the current turn

        Returns:
            int: which turn is currently active
        """

        turn = 0

        for value in self.player_1.upper_section_score.values():
            if value is not None:
                turn += 1
        for value in self.player_1.lower_section_score.values():
            if value is not None:
                turn += 1

        return turn

    def get_winner(self) -> int:
        """returns winner of game / returns 0 if none has won (for draw)

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

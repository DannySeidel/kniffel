"""
kniffel
game.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import player


class Game:
    """handles game data"""
    def __init__(self, uuid):
        self.uuid = uuid
        self.player_1 = player.Player(1)
        self.player_2 = player.Player(2)

    def get_current_turn(self) -> int:
        """..."""
        turn = 0
        for value in self.player_1.upper_section_score.values():
            if value is not None:
                turn += 1
        for value in self.player_1.lower_section_score.values():
            if value is not None:
                turn += 1

        return turn

    def get_winner(self) -> int:
        """returns id of the winner"""

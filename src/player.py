"""
kniffel
player.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

import random
import score


class Player:
    """handles player actions and data"""
    def __init__(self, player_id):
        self.player_id = player_id
        self.dice_used = []
        self.dice_put_aside = []
        self.score = score.Score()

    def throw_dice(self, n_times) -> []:
        """returns an array with n random integers between 1 and 6"""
        for _ in range(n_times):
            random_int = random.randint(1, 6)
            self.dice_used.append(random_int)

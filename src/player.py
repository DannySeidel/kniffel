"""
kniffel
player.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

from random import randint


class Player:
    """handling player actions and player score"""

    def __init__(self, player_id):
        """initializing the player

        Args:
            :param player_id: used for identification of the player
        """
        self._player_id = player_id
        self.dice_used = []
        self.dice_put_aside = []
        self.scores = dict.fromkeys(["ones", "twos", "threes", "fours", "fives", "sixes", "three_of_a_kind", "four_of_a_kind", "full_house", "small_straight",
                                     "large_straight", "yahtzee", "chance"])

    def throw_dice(self):
        """Player throwing his dices.
        Creating an array with random integers between 1 and 6"""

        dice_count = 5 - len(self.dice_put_aside)
        self.dice_used = []

        for _ in range(dice_count):
            random_int = randint(1, 6)
            self.dice_used.append(random_int)

        self.dice_used.sort()

    def get_all_possible_scores(self) -> list[int | None]:
        """returns an array with all possible scores

        Returns:
            list: array of scores or None if score already assigned
        """

        scores = [self.__get_number_score(1) if self.scores["ones"] is None else None,
                  self.__get_number_score(2) if self.scores["twos"] is None else None,
                  self.__get_number_score(3) if self.scores["threes"] is None else None,
                  self.__get_number_score(4) if self.scores["fours"] is None else None,
                  self.__get_number_score(5) if self.scores["fives"] is None else None,
                  self.__get_number_score(6) if self.scores["sixes"] is None else None,
                  self.__get_n_of_a_kind_score(3) if self.scores["three_of_a_kind"] is None else None,
                  self.__get_n_of_a_kind_score(4) if self.scores["four_of_a_kind"] is None else None,
                  self.__get_full_house_score() if self.scores["full_house"] is None else None,
                  self.__get_small_straight_score() if self.scores["small_straight"] is None else None,
                  self.__get_large_straight_score() if self.scores["large_straight"] is None else None,
                  self.__get_yahtzee_score() if self.scores["yahtzee"] is None else None,
                  self.__get_chance_score() if self.scores["chance"] is None else None]

        return scores

    def __get_number_score(self, number) -> int:
        """creating a score for a specific number/dice

        Args:
            :param number: the dice number

        Returns:
            int: score for the number
        """

        count = 0

        for value in self.dice_put_aside:
            if value == number:
                count += 1

        return count * number

    def __get_n_of_a_kind_score(self, n_times) -> int:
        """get the score for a specific of the same kind

        Args:
            :param n_times: number of times a dice number has been thrown

        Returns:
            int: score for the dices that have been thrown
        """

        most_common_dice = max(set(self.dice_put_aside), key=self.dice_put_aside.count)

        if self.dice_put_aside.count(most_common_dice) >= n_times:
            return sum(self.dice_put_aside)

        return 0

    def __get_full_house_score(self) -> int:
        """get the score of a full house

        Returns:
            int: score for the full house
        """

        dice_without_duplicates = list(dict.fromkeys(self.dice_put_aside))

        if len(dice_without_duplicates) == 2 and self.__get_n_of_a_kind_score(3) != 0 and self.__get_n_of_a_kind_score(4) == 0:
            return 25

        return 0

    def __get_small_straight_score(self) -> int:
        """get the score for a small straight

        Returns:
            int: score for the small straight
        """

        dice = self.dice_put_aside

        if (1 in dice) and (2 in dice) and (3 in dice) and (4 in dice):
            return 30
        if (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice):
            return 30
        if (3 in dice) and (4 in dice) and (5 in dice) and (6 in dice):
            return 30

        return 0

    def __get_large_straight_score(self) -> int:
        """get the score for a large straight

        Returns:
            int: score for the large straight
        """

        dice = self.dice_put_aside

        if (1 in dice) and (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice):
            return 40
        if (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice) and (6 in dice):
            return 40

        return 0

    def __get_yahtzee_score(self) -> int:
        """get the score for a yahtzee

        Returns:
            int: score for the yahtzee
        """

        dice = self.dice_put_aside

        if dice[0] == dice[1] == dice[2] == dice[3] == dice[4]:
            return 50

        return 0

    def __get_chance_score(self) -> int:
        """get the score for a chance

        Returns:
            int: score for the chance
        """

        return sum(self.dice_put_aside)

    def get_total_score(self) -> int:
        """returns the total score of the player

        Returns:
            int: total score of the player
        """

        bonus = 0
        upper_sum = self.scores["ones"] + self.scores["twos"] + self.scores["threes"] + self.scores["fours"] + self.scores["fives"] + self.scores["sixes"]

        if upper_sum >= 63:
            bonus = 35

        return sum(self.scores.values()) + bonus

    def put_dice_aside(self, value):
        """appends dice to dice_put_aside

        Args:
            :param value: the value of the dice to be put aside
        """

        self.dice_put_aside.append(value)

    def reuse_dice(self):
        """appends dice_put_aside to dice_used to reuse them"""

        self.dice_used += self.dice_put_aside
        self.dice_put_aside = []

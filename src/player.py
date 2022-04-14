"""
kniffel
player.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""

from random import randint


class Player:
    """handles player actions and data"""

    def __init__(self, player_id):
        self.player_id = player_id
        self.dice_used = []
        self.dice_put_aside = []
        self.upper_section_score = dict.fromkeys(["ones", "twos", "threes", "fours", "fives", "sixes"])
        self.lower_section_score = dict.fromkeys(["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight",
                                                  "yahtzee", "chance"])

    def throw_dice(self):
        """returns an array with random integers between 1 and 6"""

        dice_count = 5 - len(self.dice_put_aside)
        self.dice_used = []
        for _ in range(dice_count):
            random_int = randint(1, 6)
            self.dice_used.append(random_int)
        self.dice_used.sort()


    def get_all_possible_scores(self):
        """returns an array with all possible scores"""

        upper_section_scores = [self.__get_number_score(1) if self.upper_section_score["ones"] is None else None,
                                self.__get_number_score(2) if self.upper_section_score["twos"] is None else None,
                                self.__get_number_score(3) if self.upper_section_score["threes"] is None else None,
                                self.__get_number_score(4) if self.upper_section_score["fours"] is None else None,
                                self.__get_number_score(5) if self.upper_section_score["fives"] is None else None,
                                self.__get_number_score(6) if self.upper_section_score["sixes"] is None else None]

        lower_section_scores = [self.__get_n_of_a_kind_score(3) if self.lower_section_score["three_of_a_kind"] is None else None,
                                self.__get_n_of_a_kind_score(4) if self.lower_section_score["four_of_a_kind"] is None else None,
                                self.__get_full_house_score() if self.lower_section_score["full_house"] is None else None,
                                self.__get_small_straight_score() if self.lower_section_score["small_straight"] is None else None,
                                self.__get_large_straight_score() if self.lower_section_score["large_straight"] is None else None,
                                self.__get_yahtzee_score() if self.lower_section_score["yahtzee"] is None else None,
                                self.__get_chance_score() if self.lower_section_score["chance"] is None else None]

        return upper_section_scores + lower_section_scores


    def __get_number_score(self, number) -> int:
        count = 0
        for value in self.dice_put_aside:
            if value == number:
                count += 1

        return count * number


    def __get_n_of_a_kind_score(self, n_times) -> int:
        most_common_dice = max(set(self.dice_put_aside), key=self.dice_put_aside.count)
        if self.dice_put_aside.count(most_common_dice) >= n_times:
            return sum(self.dice_put_aside)

        return 0


    def __get_full_house_score(self) -> int:
        dice_without_duplicates = list(dict.fromkeys(self.dice_put_aside))
        if len(dice_without_duplicates) == 2 and self.__get_n_of_a_kind_score(3) != 0 and self.__get_n_of_a_kind_score(4) == 0:
            return 25

        return 0


    def __get_small_straight_score(self) -> int:
        dice = self.dice_put_aside
        if (1 in dice) and (2 in dice) and (3 in dice) and (4 in dice):
            return 30
        if (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice):
            return 30
        if (3 in dice) and (4 in dice) and (5 in dice) and (6 in dice):
            return 30

        return 0


    def __get_large_straight_score(self) -> int:
        dice = self.dice_put_aside
        if (1 in dice) and (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice):
            return 40
        if (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice) and (6 in dice):
            return 40

        return 0


    def __get_yahtzee_score(self) -> int:
        dice = self.dice_put_aside
        if dice[0] == dice[1] == dice[2] == dice[3] == dice[4]:
            return 50

        return 0


    def __get_chance_score(self) -> int:
        return sum(self.dice_put_aside)


    def get_total_score(self) -> int:
        """returns sum of all scores"""

        upper_section_sum = sum(self.upper_section_score.values())
        lower_section_sum = sum(self.lower_section_score.values())

        if upper_section_sum >= 63:
            upper_section_sum += 35

        return upper_section_sum + lower_section_sum


    def put_dice_aside(self, value):
        """appends dice to dice_put_aside"""

        self.dice_put_aside.append(value)


    def reuse_dice(self):
        """appends dice_put_aside to dice_used to reuse them"""

        self.dice_used += self.dice_put_aside
        self.dice_put_aside = []

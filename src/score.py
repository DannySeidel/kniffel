"""
kniffel
score.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""


class Score:
    """handles scores of one player"""
    def __init__(self):
        self.ones = None
        self.twos = None
        self.threes = None
        self.fours = None
        self.fives = None
        self.sixes = None

        self.three_of_a_kind = None
        self.four_of_a_kind = None
        self.full_house = None
        self.small_straight = None
        self.large_straight = None
        self.yahtzee = None
        self.chance = None

    def get_sum(self) -> int:
        """returns sum of all scores"""
        __upper_section_sum = self.ones + self.twos + self.threes + self.fours + self.fives + self.sixes
        __lower_section_sum = self.three_of_a_kind + self.four_of_a_kind + self.full_house + self.small_straight +\
                              self.large_straight + self.yahtzee + self.chance

        return __upper_section_sum + __lower_section_sum

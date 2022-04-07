"""
kniffel
score.py

created on 07.04.22
by Tobias Welti, Luca Kaiser, Joshua Miller, Danny Seidel
"""


class Score:
    """handles scores of one player"""
    def __init__(self):
        self.upper_section = dict.fromkeys(["ones", "twos", "threes", "fours", "fives", "sixes"])
        self.lower_section = dict.fromkeys(["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight",
                                            "yahtzee", "chance"])

    def get_sum(self) -> int:
        """returns sum of all scores"""
        upper_section_sum = sum(self.upper_section.values())
        lower_section_sum = sum(self.lower_section.values())

        if upper_section_sum >= 63:
            upper_section_sum += 35

        return upper_section_sum + lower_section_sum

    def get_current_turn(self):
        """..."""

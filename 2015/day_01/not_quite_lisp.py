# https://adventofcode.com/2015/day/1

from collections import Counter


class bracket_list():
    def __init__(self, input_file="input.txt"):
        with open(input_file) as f:
            input_data = f.read()
        self.bracket_list = input_data

    def bracket_count(self):
        """
        Counts the number of open '(' and close ')' brackets
        """
        bracket_counter = Counter(self.bracket_list)
        self.bracket_counter = bracket_counter

    def calc_floor(self):
        """
        Using the bracket counts calculate the difference between
        the open and close brackets
        """
        self.bracket_count()

        bracket_counter = self.bracket_counter
        num_open = bracket_counter['(']
        num_close = bracket_counter[')']

        floor = num_open - num_close
        return floor

    def basement_check(self):
        """
        Parses through the bracket list to determine the first character
        where the sum is negative.
        """

        bracket_list = self.bracket_list

        cur_floor = 0

        for bracket_ind in range(len(bracket_list)):
            bracket = bracket_list[bracket_ind]
            if bracket == '(':
                cur_floor += 1
            if bracket == ')':
                cur_floor -= 1
            if cur_floor == -1:
                return bracket_ind + 1


sol = bracket_list()
p1_sol = sol.calc_floor()
p2_sol = sol.basement_check()

print("part 1 solution:", p1_sol)
print("part 2 solution:", p2_sol)

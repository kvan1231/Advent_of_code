# https://adventofcode.com/2022/day/3

import string


class Rucksack():
    """
    This class will contain a list that reads in the contents of the
    rucksack
    """

    def __init__(self, file_name: str = "test.txt") -> list:
        """
        This function reads in the text file that contains the rucksack items

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().strip().split()

        # store it
        self.rucksack = raw_data

        # generate an alphabet dictionary
        all_letters = list(string.ascii_lowercase + string.ascii_uppercase)

        inv_dict = dict(enumerate(all_letters, 1))
        letter_dict = {letter: num for num, letter in inv_dict.items()}

        # store it
        self.letter_dict = letter_dict


    def part1(self) -> int:
        """
        Splits the lines at the halfway point, determines the common letter
        and maps this letter to a number, finds the sum and returns it
        """ 

        rucksack = self.rucksack
        letter_dict = self.letter_dict

        # initialize output
        priority = 0

        # loop through items in rucksack
        for item in rucksack:

            # find midpoint
            mid_point = len(item) // 2

            # find common letter
            common, = set(item[:mid_point]) & set(item[mid_point:])

            # get the value of this letter
            letter_val = letter_dict[common]

            # update priority output
            priority += letter_val

        return priority

    def part2(self) -> int:
        """
        Loops through groups of 3 lines and determines the common letter in
        these lines to calculate the total priority
        """

        rucksack = self.rucksack
        letter_dict = self.letter_dict

        # initialize output
        priority = 0

        # loop through items in rucksack
        for item_ind in range(0, len(rucksack), 3):

            # grab the lines
            item1, item2, item3 = rucksack[item_ind: item_ind + 3]

            # find common letter
            common, = set(item1) & set(item2) & set(item3)

            # get the value of this letter
            letter_val = letter_dict[common]

            # update priority output
            priority += letter_val

        return priority


def solution():
    pt1_sol = Rucksack('input.txt').part1()
    pt2_sol = Rucksack('input.txt').part2()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)



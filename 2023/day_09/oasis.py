""" https://adventofcode.com/2023/day/9 """

class Oasis():
    """
    This class contains the oasis number information used to predict the next
    value in each sequence and generate the appropriate outputs
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input file that contains the oasis number values
        

        Args:
            input_file (str, optional): the path to the text file containing
            the oasis data. Defaults to "input.txt".
        """

        # initialize the list to contain data
        num_list = []

        # read in the data
        for line in open(input_file, 'r', encoding="utf-8"):
            nums = list(map(int, line.split()))
            num_list.append(nums)

        # store the data
        self.num_list = num_list

    def _extrapolate(self, num_row:list, part1:bool = True) -> int:
        """
        Takes a row of numbers and calculating the difference in each step. If
        the entire row is 0 then just return 0, otherwise calculate the
        differences and feed back into the function to run recursively to get
        the next value in the sequence.

        Args:
            num_row (list): The list of numbers we're going to extrapolate for
            part1 (bool): Denotes if we're going to extrapolate forwards for
            part 1 "True" or backwards for part 2 "False"

        Returns:
            int: The sum of the extrapolated values
        """

        # check if the values are all 0
        if all(val == 0 for val in num_row):
            return 0

        # if they aren't then time to calculate the differences
        diffs = [
            second - first for first, second in zip(
                num_row, num_row[1:]
            )
        ]

        # feed that row into extrapolate again
        next_row = self._extrapolate(num_row=diffs, part1=part1)

        if part1:
            return num_row[-1] + next_row
        else:
            return num_row[0] - next_row            

    def calculate_sum(self, part1:bool=True) -> int:
        """
        Calculates the total extrapolated values

        Args:
            part1 (bool): Denotes if we're going to extrapolate forwards for
            part 1 "True" or backwards for part 2 "False"

        Returns:
            int: total extrapolated values using self._extrapolate
        """

        # initialize
        total_val = 0
        num_list = self.num_list

        for row in num_list:
            total_val += self._extrapolate(row, part1)

        return total_val

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Oasis('input.txt').calculate_sum()
    pt2_sol = Oasis('input.txt').calculate_sum(part1=False)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

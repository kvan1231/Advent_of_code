""" https://adventofcode.com/2023/day/3 """

class Schematic():
    """
    Class representing the gondola schematic diagram
    """
    def __init__(self, input_file:str = 'input.txt') -> None:
        """
        Takes the input text file and converts it into a grid
        containing all of the numbers and symbols in the schematic.
        Scans through the grid and stores the coordinates of the
        numbers in the grid adjacent to a symbol.

        Args:
            input_file (str, optional): The text file containing the
            schematic. Defaults to 'input.txt'.
        """

        # read in the grid
        schematic_grid = open(input_file, "r").read().splitlines()

        # store it
        self.schematic_grid = schematic_grid

    def sum_parts(self) -> int:
        """
        Scans through the coordinates of the numbers adjacent
        to the symbols and sums up the parts numbers found

        Returns:
            int: the sum of the parts numbers
        """

        # load
        schematic_grid = self.schematic_grid

        # find the positions of the numbers and store those coordinates
        coord_set = set()

        # initilize a list of parts
        parts_list = []

        # loop through the rows and columns to find a symbol
        for row_ind, row in enumerate(schematic_grid):
            for col_ind, character in enumerate(row):
                
                # check if the character is a digit (not a symbol)
                if character.isdigit() or character == ".":
                    continue

                # check adjacent cells
                for cur_row in [row_ind - 1, row_ind, row_ind + 1]:
                    for cur_col in [col_ind - 1, col_ind, col_ind + 1]:
                        # check cell for out of bounds and if not digit
                        if (
                            (cur_row < 0 or cur_row >= len(schematic_grid)) or
                            (cur_col < 0 or cur_col >= len(schematic_grid[cur_row])) or
                            not schematic_grid[cur_row][cur_col].isdigit()
                        ):
                            continue
                        # if it is a digit and inbounds, scan for the beginning of the number
                        while cur_col > 0 and schematic_grid[cur_row][cur_col - 1].isdigit():
                            # move left
                            cur_col -= 1
                        coord_set.add((cur_row, cur_col))

        # scan through to get the numbers
        for row, col in coord_set:
            # initialize the part number in string format
            part_string = ""

            # if we have found a digit, scan left to find entire number
            while (
                col < len(schematic_grid[row]) and
                schematic_grid[row][col].isdigit()
            ):
                # add digit to parts string and step right
                part_string += schematic_grid[row][col]
                col += 1

            # add part to list
            parts_list.append(int(part_string))

        return sum(parts_list)
                
    def gear_ratios(self) -> int:
        """
        Finds the locations of the gears denoted by * and calculates
        the product of the two numbers adjacent to produce a gear ratio.
        Returns the sum of all gear ratios.

        Returns:
            int: The sum of all gear ratios calculated
        """

        # load
        schematic_grid = self.schematic_grid

        # initialize the output
        gear_ratio_prod = 0

        # loop through the rows and columns to find a symbol
        for row_ind, row in enumerate(schematic_grid):
            for col_ind, character in enumerate(row):
                
                # check if the character is a gear
                if character != "*":
                    continue
                
                # initialize a temporary set for when we encounter a gear
                temp_gear_set = set()

                # check adjacent cells
                for cur_row in [row_ind - 1, row_ind, row_ind + 1]:
                    for cur_col in [col_ind - 1, col_ind, col_ind + 1]:
                        # check cell for out of bounds and if not digit
                        if (
                            (cur_row < 0 or cur_row >= len(schematic_grid)) or
                            (cur_col < 0 or cur_col >= len(schematic_grid[cur_row])) or
                            not schematic_grid[cur_row][cur_col].isdigit()
                        ):
                            continue
                        # if it is a digit and inbounds, scan for the beginning of the number
                        while cur_col > 0 and schematic_grid[cur_row][cur_col - 1].isdigit():
                            # move left
                            cur_col -= 1
                        temp_gear_set.add((cur_row, cur_col))

                # if the gear has more than one adjacent number then we have a ratio
                if len(temp_gear_set) != 2:
                    continue

                # initilize a temp list to store parts
                parts_list = []

                # scan through to get the numbers
                for row, col in temp_gear_set:
                    # initialize the part number in string format
                    part_string = ""

                    # if we have found a digit, scan left to find entire number
                    while (
                        col < len(schematic_grid[row]) and
                        schematic_grid[row][col].isdigit()
                    ):
                        # add digit to parts string and step right
                        part_string += schematic_grid[row][col]
                        col += 1

                    # add part to list
                    parts_list.append(int(part_string))

                # find the product of the two parts and add that to the output
                gear_ratio_prod += parts_list[0] * parts_list[1]

        # return
        return gear_ratio_prod

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = Schematic('input.txt').sum_parts()
    pt2_sol = Schematic('input.txt').gear_ratios()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

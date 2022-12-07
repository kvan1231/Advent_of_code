# https://adventofcode.com/2022/day/5

import re
import string


class Stacks():
    """
    This class will contain a list that reads in the input containing the
    initial stack setup and the instructions
    """

    def __init__(self, file_name: str = "test.txt") -> list:
        """
        This function reads in the text file that contains the stacks and the
        instructions

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().split('\n\n')

        raw_stacks, raw_instructions = raw_data

        # grab only the numbers
        instruction_list = [
            int(num) for num in re.findall(r"\d+", raw_instructions)
        ]

        # convert it to a list of tuples to be read from
        instructions = [
            tuple(instruction_list[i:i+3])
            for i in range(0, len(instruction_list), 3)
        ]

        # store it
        self.instructions = instructions

        # initialize the stacks list
        stacks = []

        # loop through raw stacks data
        for index, char in enumerate(
            zip(*map(list, raw_stacks.split("\n")[::-1]))
            ):
            try:
                int(char[0])
                # print(char[1:])
                stacks.append(''.join(char[1:]))
            except ValueError:
                pass

        stacks = [list(char.strip(' ')) for char in stacks]

        # store it
        self.stacks = stacks

    def move_stack(self) -> str:
        """
        This function handles moving the stacked crates around based on the
        instructions ingested by popping off the top crate and moving it to
        the new position then returns the top crates in each position as
        a string
        """

        # get the instructions and stacks
        instructions = self.instructions
        stacks = self.stacks

        # loop through the instructions
        for num_items, from_pos, to_pos in instructions:
            # move the item
            for item in range(num_items):
                moved_item = stacks[from_pos - 1].pop()
                stacks[to_pos - 1].append(moved_item)

        # get the top character in each stack
        top_chars = ''.join(item[-1] for item in stacks)

        # output
        return top_chars

    def move_stack_cm9001(self) -> str:
        """
        This function handles moving the stacked crates around based on the
        instructions ingested by moving the whole stack of N items to
        the new position then returns the top crates in each position as
        a string
        """

        temp_items = []

        # get the instructions and stacks
        instructions = self.instructions
        stacks = self.stacks

        # loop through the instructions
        for instruction in instructions:
            num_items = instruction[0] * -1
            from_pos = instruction[1] - 1
            to_pos = instruction[2] -1

            # move the items to a temporary list
            temp_items = stacks[from_pos][num_items:]

            # delete them from original list
            del stacks[from_pos][num_items:]

            # readd them back
            stacks[to_pos].extend(temp_items)

            # clear temp
            temp_items = []

        # get the top character in each stack
        top_chars = ''.join(item[-1] for item in stacks)

        # output
        return top_chars


def solution():
    pt1_sol = Stacks('input.txt').move_stack()
    pt2_sol = Stacks('input.txt').move_stack_cm9001()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

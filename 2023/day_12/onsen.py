""" https://adventofcode.com/2023/day/12 """

class ConditionRecords():
    """
    This class contains the functions related to the conditions
    of the various hot springs
    """

    def __init__(self, input_file:str = "input.txt", p2:bool = False) -> None:
        """
        Reads in the input file that contains the conditions of the hot springs

        Args:
            input_file (str, optional): the path to the text file containing
            the hot spring data. Defaults to "input.txt".
            p2 (bool, optional): A boolean controlling if this is part 1 or
            part 2 of the question. Defaults to False
        """

        # initialize the lists
        condit_list = []
        contig_list = []

        # read in the data
        for line in open(input_file, 'r', encoding='utf-8'):
            temp_cond, temp_cont = line.split()

            contig_tuple = tuple(map(int, temp_cont.split(",")))

            # if we're solving part 2 then we need to duplicate the data 5x
            if p2:
                temp_cond = "?".join([temp_cond] * 5)
                contig_tuple *= 5

            condit_list.append(temp_cond)
            contig_list.append(contig_tuple)

        # store the data
        self.conditions = condit_list
        self.contiguous = contig_list

        # create a cache for results to speed up calculation
        self.cached_res = {}

    def gen_combination(self, condit:str, contig:tuple) -> int:
        """
        Generates the total number of possible combination of the hot springs
        based on the conditions and the number of contiguous damaged springs given

        Args:
            condit (str): A string containing the various conditions of the springs
            contig (tuple): A tuple containing the number of damaged contiguous springs

        Returns:
            int: The total number of possible combination
        """

        # initialize
        num_combos = 0

        # generate the key combo for cached results
        cache_key = (condit, contig)

        # check if this combination has been caculated before
        if cache_key in self.cached_res:
            return self.cached_res[cache_key]

        # for edge cases
        # empty condition string, no more springs
        if condit == "":
            # expect empty contiguous tuple, 1 combo otherwise return 0
            return 1 if contig == () else 0

        # empty contiguous tuple
        if contig == ():
            # expect no springs, if we have a broken one, return 0 otherwise, 1
            return 0 if '#' in condit else 1

        # now to loop through the possible cases recursively
        # if we have a broken spring then we have the start of a block of broken springs
        if condit[0] in "#?":
            # check if the block is valid based on
            # 1. do we have enough springs left for the block
            # 2. all of the springs within the first n blocks must be broken
            # 3. the next itme right after the block must not be a broken spring
            if (
                contig[0] <= len(condit) and
                "." not in condit[:contig[0]] and
                (contig[0] == len(condit) or condit[contig[0]] != "#")
            ):
                num_combos += self.gen_combination(condit[contig[0] + 1:], contig[1:])

        # if the condition string starts with a working spring
        if condit[0] in ".?":
            num_combos += self.gen_combination(condit[1:], contig)

        # add this result to the cached result
        self.cached_res[cache_key] = num_combos

        return num_combos

    def calc_total_combinations(self) -> int:
        """
        Calculates and outputs the total number of possible combinations from the input

        Returns:
            int: the total number of possible combinations for the inputted hot spring data
        """

        # initialize
        total_combinations = 0

        # grab the data
        conditions = self.conditions
        contiguous = self.contiguous

        for row_index, cond_row in enumerate(conditions):
            # cond_row = conditions[row_index]
            cont_row = contiguous[row_index]

            total_combinations += self.gen_combination(cond_row, cont_row)

        return total_combinations

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = ConditionRecords().calc_total_combinations()
    pt2_sol = ConditionRecords(p2=True).calc_total_combinations()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

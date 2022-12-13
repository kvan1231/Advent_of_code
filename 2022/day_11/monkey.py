# https://adventofcode.com/2022/day/11

from copy import deepcopy
from math import prod


class Monkey():
    """
    Contains all of the information related to a monkey and its current
    state
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the monkeys
        properties

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # initialize lists we're going to populate
        id_list = []
        item_list = []
        operator_list = []
        divisible_list = []
        true_list = []
        false_list = []

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().strip().split('\n\n')

        # pull out the numbers from each line and append to the lists
        for raw_monkey in raw_data:
            temp_id, items, ops, divs, t_cond, f_cond = raw_monkey.split('\n')
            # monkey id
            id_list.append(
                int(temp_id.split()[-1].strip(":"))
            )
            # the list of items
            item_list.append(
                [int(item) for item in items.split(':')[1].split(',')]
            )
            # we need to use lambda to create a list of functions
            operation = ''.join(ops.split()[-3:])
            operator_list.append(
                lambda old, operation=operation: eval(operation)
            )
            # the number we're checking if its divisible by
            divisible_list.append(
                int(divs.split()[-1])
            )
            # the index of the monkey we'll throw to if it is divisible
            true_list.append(
                int(t_cond.split()[-1])
            )
            # the index of the monkey we'll throw to if it isnt divisible
            false_list.append(
                int(f_cond.split()[-1])
            )

        # put it all into one list
        monkey_vals = [
            id_list, item_list, operator_list,
            divisible_list, true_list, false_list
        ]

        # store
        self.monkeys = monkey_vals

    def simulate(self, n_rounds: int = 20, part: int = 1) -> int:
        """
        Simulates n_rounds of the monkeys interactions and returns the
        product of the two highest number of item inspections over this time

        Parameters
        ----------
        n_rounds: int
            The number of rounds we're going to simulate
        part: int
            The part of the question we're going to simulate, 1 or 2

            In part 2 we're only interested in whether or not the item number
            is divisible by the divisors of each monkey. To avoid the item
            number from blowing up we're going to take the modulus of the item
            number with respect to the product of ALL of the monkeys divisors.
            This will prevent the item value from growing too large.

        Returns
        -------
        monkey_business: int
            The product of the two most active monkeys
        """

        # read in the data
        monkeys = deepcopy(self.monkeys)

        # split the data
        monkey_id, item_list, operator_list, \
            divisible_list, true_list, false_list = monkeys

        # create a list to track the amount of activity per monkey
        activity = [0 for _ in range(len(monkey_id))]

        total_div = prod(divisible_list)

        # loop over the rounds
        for _ in range(n_rounds):

            # loop over the monkeys
            for monkey_ind in range(len(monkey_id)):

                # loop over the items
                for item in item_list[monkey_ind]:

                    # increment the amount of activity of this monkey
                    activity[monkey_ind] += 1

                    # get the operator associated
                    operator = operator_list[monkey_ind]

                    # calculate the items new value
                    item = operator(item)

                    # if part 1 then divide by 3
                    if part == 1:
                        item = item // 3
                    # otherwise
                    else:
                        item = item % total_div

                    # check if divisible by monkey number
                    div_val = divisible_list[monkey_ind]

                    # determine which monkey to toss it to
                    if item % div_val == 0:
                        new_monkey = true_list[monkey_ind]
                    else:
                        new_monkey = false_list[monkey_ind]

                    # toss it to the new monkey
                    item_list[new_monkey].append(item)

                # remove the item
                item_list[monkey_ind] = []

        # sort the activity list
        activity.sort()

        # calculate the product of the top 2
        monkey_business = prod(activity[-2:])

        return monkey_business


def solution():
    pt1_sol = Monkey('input.txt').simulate()
    pt2_sol = Monkey('input.txt').simulate(n_rounds=10000, part=2)
    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

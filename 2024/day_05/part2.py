""" https://adventofcode.com/2024/day/5 """

import functools

def _check_ordered(stack: list, ordering: dict) -> bool:
    """Checks if a given stack is in the correct order

    Parameters
    ----------
    stack : list
        The input stack of numbers
    ordering : dict
        The ordering rules for the numbers

    Returns
    -------
    bool
        Whether or not the stack is in the correct order
    """

    # loop through the stack
    for i, left in enumerate(stack):
        # get the right number
        for right in stack[i + 1:]:
            order_bool = (left, right)
            if order_bool in ordering and ordering[order_bool] == 1:
                return False
    return True

def make_comparator(ordering: dict):
    """Return a cmp-style comparator that uses the given ordering map."""
    def _comparitor(left: int, right: int) -> int:
        return ordering.get((left, right), 0)
    return _comparitor

def print_queue(input_path: str) -> int:
    """Reads in the file and the sum of the middle values of each row
    in the print queue

    Parameters
    ----------
    input_path : str
        The path to the input file
    """

    # read in the raw data
    raw_data = open(input_path, "r", encoding='utf-8').read()

    order_data, stack_data = raw_data.split("\n\n")

    # initilize the rules to sort numbers
    order = []

    # split the raw data into order rules and print stacks
    for line in order_data.splitlines():
        # split our lines to get our order rules
        order.append(list(map(int, line.split("|"))))

    # initalize the order map
    order_map = {}

    # create the order map
    for n1, n2 in order:
        # correct order
        order_map[(n1, n2)] = -1
        # incorrect order
        order_map[(n2, n1)] = 1

    # get the comparator function
    comparator = make_comparator(order_map)

    summed_value = 0

    # loop through each stack
    for line in stack_data.splitlines():
        stack = list(map(int, line.split(",")))
        # check if the stack is not in the correct order
        if not _check_ordered(stack, order_map):
            stack.sort(key=functools.cmp_to_key(comparator))
            summed_value += stack[len(stack) // 2]

    return summed_value

print(print_queue("input.txt"))

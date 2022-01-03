# https://adventofcode.com/2015/day/12

import re
import json


def read_data(input_file='input.txt'):
    """
    Read in the accounting data
    """

    with open(input_file) as f:
        raw_data = f.read()

    return raw_data


def simple_calc(acc_data):
    """
    Performs the simple summation of all numbers in the
    accounting data
    """

    # pull out all of the numbers in the data using regex
    acc_nums = map(int, re.findall("-?[0-9]+", acc_data))

    # sum these numbers
    acc_sum = sum(acc_nums)
    return acc_sum


def ignore_red(obj):
    """
    Create a hook for json.loads to ignore certain things
    """

    # if the value contains red then ignore
    if "red" in obj.values():
        return {}

    # otherwise just return the value
    else:
        return obj


def filter_non_reds(acc_data):
    """
    Remove the non red values from the data and output the accounting data
    """

    # use the json.load to ignore the red values
    no_reds = json.loads(acc_data, object_hook=ignore_red)

    # convert bck to str
    filtered_data = str(no_reds)

    # output
    return filtered_data


def sol_pipeline():
    """
    Run the commands in order to output the solutions to each part
    """
    acc_data = read_data()
    p1_sol = simple_calc(acc_data)

    no_red_data = filter_non_reds(acc_data)
    p2_sol = simple_calc(no_red_data)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)

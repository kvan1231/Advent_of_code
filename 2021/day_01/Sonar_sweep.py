# https://adventofcode.com/2021/day/1

import pandas as pd


def read_input(file_name="test.txt"):
    """
    This function reads in a text file that contains a list of integers
    and returns it as a pandas series.
    """

    # Read in the file, remember to set header=None or we'll miss the first row
    input_array = pd.read_csv(file_name, header=None)
    return input_array


def num_increase(file_name="test.txt"):
    """
    This function is going to calculate the number of times the
    subsequent number in an array is larger than the previous number
    and print out this value.
    """

    # Get the input
    input_array = read_input(file_name)

    # Subtract the array from one another and sum where the result is positive
    num_inc = (input_array > input_array.shift()).sum()

    # Print the solution
    print(num_inc)


def rolling_increase(file_name="test.txt"):
    """
    Similar to the function num_increase, we're also going to calculate
    the number of times the subsequent number in an array is larger than
    the previous number. The trick here is that we're going to first
    calculate a sum of a three-measurement sliding window.
    """

    # Get the input
    input_array = read_input(file_name)

    # Get the sum of the three-measurement window
    summed_array = input_array.rolling(3).sum()

    # Subtract the array from one another and sum where the result is positive
    num_inc = (summed_array > summed_array.shift()).sum()

    # Print the solution
    print(num_inc)
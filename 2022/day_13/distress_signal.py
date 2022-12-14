# https://adventofcode.com/2022/day/13

from ast import literal_eval
from functools import cmp_to_key
from math import prod


class Signal():
    """
    Contains the pairs of packets that represent the distress signal
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the packets

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # we're going to use ast.literal_eval as its safer than using
        # python eval

        packets = [
            [*map(literal_eval, line.split())] for line in
            open(file_name).read().split('\n\n')
        ]

        self.packets = packets

    def compare(self, left, right):
        """
        Compares the left and right pairs to determine if they are in the
        right order or not. We're going to be using the match - case
        statements to do this.
        """

        match left, right:
            # If both values are integers
            case int(), int():
                """
                - If the left integer is lower than the right integer,
                the inputs are in the right order, return 1

                - If the left integer is higher than the right integer,
                the inputs are not in the right order, return -1

                - Otherwise, the inputs are the same integer;
                continue checking the next part of the input, return 0
                """
                # Do some boolean math since output is (-1, 0, 1)
                return (left > right) - (left < right)

            # If both values are lists
            case list(), list():

                # compare the values of each list
                for tmp_val in map(self.compare, left, right):
                    if tmp_val:
                        return tmp_val
                # compare lengths of the lists
                # if the left runs out first len(left) > len(right) return 1
                return self.compare(len(left), len(right))

            # If one is an integer and the other is a list
            # convert the integerto a list and continue
            case int(), list():
                return self.compare([left], right)
            case list(), int():
                return self.compare(left, [right])

    def sum_pairs(self) -> int:
        """
        Returns the total sum of the indices of all packets that are in the
        right order.
        """

        packets = self.packets

        # compare the packets and return a list of the indexes that are
        # in the right order
        correct_inds = [
            ind for ind, pair in enumerate(packets, 1) if
            self.compare(*pair) == -1
        ]

        # sum the indices
        summed_vals = sum(correct_inds)

        return summed_vals

    def sorted_packets(self) -> int:
        """
        Sorts the packets and returns the product of the indices
        """

        packets = self.packets

        # add the 2 and the 6 to the packet list
        padded_packets = sum(packets, [[2], [6]])

        # sort the packets
        sort_pkts = sorted(padded_packets, key=cmp_to_key(self.compare))

        # find the indices
        divider_inds = [
            ind for ind, pair in enumerate(sort_pkts, 1) if pair in [[2], [6]]
        ]

        prod_vals = prod(divider_inds)

        return prod_vals


def solution():
    pt1_sol = Signal('input.txt').sum_pairs()
    pt2_sol = Signal('input.txt').sorted_packets()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

# https://adventofcode.com/2022/day/5


class Signal():
    """
    This class will contain a string representing a signal sequence
    """

    def __init__(self, file_name: str = "test.txt") -> list:
        """
        This function reads in the text file that contains the signal

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.readline().strip()

        self.signal = raw_data

    def start_marker(self, N=4) -> int:
        """
        Finds the index where the string sequence contains N unique
        characters
        """

        signal = self.signal

        # loop through the data
        for index in range(N, len(signal)):
            sub_sig = signal[index - N:index]

            # if there are N unique characters, return
            if len(set(sub_sig)) == N:
                return index


def solution():
    pt1_sol = Signal('input.txt').start_marker(N=4)
    pt2_sol = Signal('input.txt').start_marker(N=14)

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)



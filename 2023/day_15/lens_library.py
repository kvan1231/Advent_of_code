""" https://adventofcode.com/2023/day/15 """

class LensLibrary():
    """
    A class containing the data for the lens library
    """

    def __init__(self, input_file:str = "input.txt") -> None:
        """
        Reads in the input file and extracts the raw data

        Parameters
        ----------
        input_file : str, optional
            The text file containing the initialization sequence that we will
            parse and decode, by default "input.txt"
        """

        # read in the data as a csv
        sequence = open(
            input_file, 'r', encoding='utf-8'
        ).read().strip().split(',')

        # keep the sequence
        self.seq = sequence

    def calculate_sum(self) -> int:
        """
        Calculates the sum of the input file after converting the comma separated
        strings and converting them into numbers using the hash algorithm

        Returns
        -------
        int
            The sum of the input file
        """

        # initialize
        sequence = self.seq
        output_value = 0

        # loop through the sequences to convert the strings to integers
        for sub_seq in sequence:
            temp_val = self._hash_algorithm(sub_seq)

            # sum the values
            output_value += temp_val

        return output_value

    def hashmap(self) -> int:
        """
        Uses the inputted sequence and places values in one of 0-255 boxes using
        the algorithm and calculates the sum of these boxes

        Returns
        -------
        int
            The output value based on the algorithm
        """

        # load in the sequence
        sequence = self.seq

        # create the boxes to be populated
        boxes = [[] for _ in range(256)]

        # create the focal lengths that would exist in each box to be populated
        focal_lengths = {}

        # loop through the sequence to determine what to do
        for sub_seq in sequence:

            # if the subsequence has a -
            if "-" in sub_seq:
                # get the box label from the subsequence
                box_label = sub_seq[:-1]

                # convert it to a number using the algorithm
                box_index = self._hash_algorithm(box_label)

                # remove any values inside the box
                if box_label in boxes[box_index]:
                    boxes[box_index].remove(box_label)

            # otherwise if it contains a =
            else:
                # split the subsequence at =
                box_label, focal_length = sub_seq.split("=")

                # convert box label to index
                box_index = self._hash_algorithm(box_label)

                # add that label to the boxes if it isn't there
                if box_label not in boxes[box_index]:
                    boxes[box_index].append(box_label)

                # add the focal to our dictonary
                focal_lengths[box_label] = int(focal_length)

        # initialize the output value
        output_value = 0

        # calculate the output integer by looping through the boxes
        for box_number, box in enumerate(boxes, 1):
            # loop through the items in the box
            for lens_slot, box_label in enumerate(box, 1):
                # time for some math
                output_value += box_number * lens_slot * focal_lengths[box_label]

        return output_value

    def _hash_algorithm(self, string:str) -> int:
        """
        Takes the read in string and uses the algorithm to convert this string
        into an integer

        Parameters
        ----------
        string : str
            The input value that the algorithm will convert to an integer

        Returns
        -------
        int
            the converted integer produced when applying the algorithm to a sequence
        """
        # initialize
        output_value = 0

        for character in string:
            output_value += ord(character)
            output_value *= 17
            output_value %= 256

        return output_value

def solution():
    """
    Summary output function that spits out the solutions
    """
    pt1_sol = LensLibrary().calculate_sum()
    pt2_sol = LensLibrary().hashmap()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

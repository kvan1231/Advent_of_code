# https://adventofcode.com/2021/day/3

import pandas as pd


class BinaryDiagnostic():
    """
    Takes an input file that consists of 0s and 1s and
    converts it into a power consumption value.

    Inputs
    ------
    file_name : string
        The name of the input file to be read in
    """

    def __init__(self, file_name="test.txt"):
        """
        This function reads in the text file that contains a
        grid of 1s and 0s. There is no header or delimiter in
        this file so since we're only using pandas we need to
        read in the data and then split it. Also note that because
        the values are all 0s and 1s we need to read the values
        in as a string so leading 0s aren't dropped.
        """
        self.file_name = file_name

        # Read in the file using our header and specify the delimiter as space
        temp_df = pd.read_csv(self.file_name, header=None, dtype=str)

        # The data has been read in as a single column so we need to split it
        temp_vals = temp_df[0].values

        self.input_df = pd.DataFrame(data=[list(val) for val in temp_vals])

    def gamma_rate(self):
        """
        The gamma rate is determined by finding the most common bit
        in a corresponding column, which results in a binary number.
        This binary number is then converted to a decimal value.
        """

        gamma_df = self.input_df

        # Find the most common bit in a row using mode
        common_bit = gamma_df.mode()

        # Adding strings in python just removes whitespace
        gamma_binary = common_bit.sum().sum()

        # convert the binary number to a decimal
        gamma_int = int(gamma_binary, 2)

        # store the values
        self._gamma_bin = gamma_binary
        self.gamma = gamma_int

    def epsilon_rate(self):
        """
        The epsilon rate is the inverse of the gamma rate in binary
        that is then converted to a decimal value.
        """

        # Make sure we've gotten the gamma value in binary
        self.gamma_rate()
        self._gamma_bin

        # Invert it
        eps_binary = ''.join('1' if bit == '0' else '0'
                            for bit in self._gamma_bin)

        # convert the binary number to a decimal
        eps_int = int(eps_binary, 2)

        # store the values
        self._eps_bin = eps_binary
        self.epsilon = eps_int

    def power_consumption(self):
        """
        The power consumption of the submarine is given by
        epsilon * gamma
        """

        # Make sure gamma and epsilon have been calculated
        self.epsilon_rate()

        gamma = self.gamma
        epsilon = self.epsilon

        power_comp = gamma * epsilon
        print(power_comp)

    def oxygen_rate(self):
        """
        To find oxygen generator rating, determine the most common
        value (0 or 1) in the current bit position, and keep only
        numbers with that bit in that position. If 0 and 1 are equally
        common, keep values with a 1 in the position being considered.
        """

        oxygen_df = self.input_df

        # Need to loop through all of the positions
        for position in oxygen_df.columns:
            # Get the most common bit in that column
            common_bit = oxygen_df[position].mode()

            # If 0 and 1 are equally common then both values will appear
            # in the mode and the length of the output will be > 1
            if len(common_bit) > 1:
                # Keep all of the rows where the position contains a 1
                oxygen_df = oxygen_df[oxygen_df[position].values == "1"]
            else:
                # pull the value of the most common bit
                bit_val = common_bit.values[0]
                # Keep the most common bit
                oxygen_df = oxygen_df[oxygen_df[position].values == bit_val]
            
            # Stop the loop if we're on the last row
            if len(oxygen_df) == 1:

                # calculate the oxygen rate and store it
                oxygen_binary = oxygen_df.iloc[0].sum()
                oxygen_rate = int(oxygen_binary, 2)
                self.oxygen = oxygen_rate
                break

    def C02_scrubber_rate(self):
        """
        To find C02 scrubber rating, determine the least common
        value (0 or 1) in the current bit position, and keep only
        numbers with that bit in that position. If 0 and 1 are equally
        common, keep values with a 1 in the position being considered.
        """

        C02_df = self.input_df

        # Need to loop through all of the positions
        for position in C02_df.columns:
            # Get the most common bit in that column
            common_bit = C02_df[position].mode()
            # If 0 and 1 are equally common then both values will appear
            # in the mode and the length of the output will be > 1
            if len(common_bit) > 1:
                # Keep all of the rows where the position contains a 0
                C02_df = C02_df[C02_df[position].values == "0"]
            else:
                # pull the value of the most common bit and flip it
                bit_val = str(1 - int(common_bit.values[0]))
                # Keep the most common bit
                C02_df = C02_df[C02_df[position].values == bit_val]
            
            # Stop the loop if we're on the last row
            if len(C02_df) == 1:

                # calculate the oxygen rate and store it
                C02_binary = C02_df.iloc[0].sum()
                C02_rate = int(C02_binary, 2)
                self.C02 = C02_rate
                break

    def life_support_rating(self):
        """
        The life support rating of the submarine is given by
        oxygen_rating * C02_scrubber_rating
        """

        # Make sure gamma and epsilon have been calculated
        self.oxygen_rate()
        self.C02_scrubber_rate()

        oxygen = self.oxygen
        C02 = self.C02

        ls_rating = oxygen * C02
        print(ls_rating)
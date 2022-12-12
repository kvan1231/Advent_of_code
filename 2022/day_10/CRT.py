# https://adventofcode.com/2022/day/9


class Cycle():
    """
    This class will contain the signals being inputted to the system
    """

    def __init__(self, file_name: str = "test.txt") -> None:
        """
        This function reads in the text file that contains the execution used
        to calculate the signal strength

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().strip().split('\n')

        """
        the raw instructions only come in two types of commands
            - addx V takes two cycles to complete. After two cycles,
            the X register is increased by the value V. (V can be negative.)
            - noop takes one cycle to complete. It has no other effect.
        """

        # to make life easier, we're going to find all of the addx commands
        # and pad them so that the cycles match up with the row

        # create an empty list to contain our new program
        padded_program = []

        # loop through the lines in the raw commands
        for command in raw_data:

            # check if the command is addx
            cmnd_type = command.split()
            if cmnd_type[0] == 'addx':

                # pad
                padded_program.append('noop')
            padded_program.append(command)

        # save the instructions
        self.program = padded_program

    def signal_output(self) -> list:
        """
        Calculates the signal strength based on the inputted program
        """

        # initialize
        signal_sum = 0
        register = 1
        cycle = 0
        pixel_pos = 0
        line = ''

        output_image = []

        # load program
        program = self.program

        # we take the values at specific cycles
        calc_cycles = (20, 60, 100, 140, 180, 220)

        for command in program:
            cycle += 1

            # light up appropriate pixels in the line
            if pixel_pos in (register - 1, register, register + 1):
                pixel = '█'
            else:
                pixel = ' '
            line += pixel

            # if we're at a specific cycle
            if cycle in calc_cycles:
                # increase signal sum
                signal_strength = cycle * register
                signal_sum += signal_strength

            cmnd_type = command.split()

            # if the command is addx
            if cmnd_type[0] == 'addx':
                value = int(cmnd_type[1])

                # increase register
                register += value

            # move the pixel
            pixel_pos += 1

            # if we're at the end of the line that is 40 wide
            if pixel_pos % 40 == 0:
                # add the line to our output image
                output_image.append(line)

                # reset the line and pixel
                line = ''
                pixel_pos = 0

        total_output = [signal_sum, output_image]

        return total_output


def solution():
    pt1_sol, pt2_sol = Cycle('input.txt').signal_output()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)

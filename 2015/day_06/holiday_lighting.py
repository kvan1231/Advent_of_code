# https://adventofcode.com/2015/day/6

import numpy as np


def light_sim(input_file="input.txt", part=1):
    light_array = np.zeros((1000, 1000), dtype=np.int8)

    # read in all of the data
    with open(input_file, 'r') as input:
        instruction_list = [line.split() for line in input]

    # loop through
    for command in instruction_list:
        x1, y1 = command[-3].split(',')
        x2, y2 = command[-1].split(',')
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # if its part 1 we just want to check if the light is on
        if part == 1:
            # if the command is to toggle we're going to use the xor command
            if command[0] == 'toggle':
                light_array[x1:x2+1, y1:y2+1] ^= 1

            # otherwise set the value to 0 or 1
            else:
                light_array[x1:x2+1, y1:y2+1] = ['off', 'on'].index(command[1])

        # if its part 2 then depending on the command we change the value
        else:
            if command[0] == 'toggle':
                light_array[x1:x2+1, y1:y2+1] += 2

            elif command[1] == 'on':
                light_array[x1:x2+1, y1:y2+1] += 1

            elif command[1] == 'off':
                light_array[x1:x2+1, y1:y2+1] -= 1

                # the array cannot be negative
                light_array[light_array < 0] = 0

    return light_array


lights = light_sim()
num_lights = lights.sum().sum()
print("Part 1: ", num_lights)

inc_lights = light_sim(part=2)
light_brightness = inc_lights.sum().sum()
print("Part 2: ", light_brightness)


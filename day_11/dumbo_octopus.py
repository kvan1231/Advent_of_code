# https://adventofcode.com/2021/day/11

import numpy as np
from scipy import signal


# read in the file, just learned about np.genfromtxt
# which is a much more efficient way to read in a block
# of numbers
input_file = 'input.txt'
init_energy = np.genfromtxt(
    input_file, delimiter=1, dtype=np.int32
)

# make a copy of the energy to avoid issues
energy = init_energy.copy()

# create a grid of zeros to keep track of the number of
# flashes
flash_grid = np.zeros(init_energy.shape).astype(np.int32)

# create a 3x3 matrix that adds energy if a cell flashes
energy_spread = np.ones((3, 3))

# create a temp matrix that holds the new energy level
# after each step
new_energy = energy.copy()

# initalize the count of number of flashes
num_flashes = 0

# start the day count at 0
day = 0

# changed for part 2, wrap entire loop
# in a while loop to get second solution
while True:
    # print(day)
    day += 1
    # add energy
    energy += 1

    # find where flashes occur
    flash_points = energy > 9

    # create a flag to check flashes, set to false
    # when checks are done
    check_flash_flag = True

    while check_flash_flag:
        # spread out the flash energy
        flash_spread = (
            signal.convolve(flash_points, energy_spread, mode='same')
            .astype(np.int32)
        )
        # replace our temp array
        new_energy = energy + flash_spread

        # check if there are any new flashes
        new_flash_points = new_energy > 9
        flash_overlap = (new_flash_points & ~flash_points).sum().sum()

        # change flag if necessary
        check_flash_flag = flash_overlap > 0

        # update flash points
        flash_points = new_flash_points

    # replace energy array
    energy = new_energy

    # set the points that flashed to 0 
    energy[flash_points] = 0

    # update flash count
    flash_count = new_flash_points.sum().sum()
    num_flashes += flash_count
    if day == 100:
        day100_flash_count = num_flashes

    if flash_points.all().all():
        # flash_count, day_step
        all_flash_day = day
        all_flash_count = flash_count
        break

print("part 1 solution:", day100_flash_count)
print("part 2 solution:", all_flash_day)

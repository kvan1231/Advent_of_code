# https://adventofcode.com/2021/day/9

import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import measurements

# part 1 wants us to find areas where we have a local minima
# luckily we can use some premade packages to make this
# straightforward

# read in the input
heights = []
file_name = "input.txt"
for line in open(file_name, 'r').readlines():
    row = [int(num) for num in line.strip()]
    heights.append(row)

# We're going to be using scipy.signal.find_peaks which
# doesn't work well with edges so we're going to pad
# the edges with 9s since 9 is our maximum value

heights_array = np.array(heights)
padded_heights = np.pad(
    heights_array, pad_width=1, constant_values=9
)

# get the dimensions of the padded array
padded_size = padded_heights.shape
num_rows = padded_size[0]
num_cols = padded_size[1]

# use the padded size to create an identical empty
# array to contain our flags denoting if we have a min
min_flag = np.zeros(padded_size)

# now lets loop through the rows and find any local minima
for row_ind in range(num_rows):
    # multiply our heights by -1 to turn minima into maxima
    temp_cols = find_peaks(-1 * padded_heights[row_ind])
    min_flag[row_ind, temp_cols[0]] += 1

# do the same thing for columns
for col_ind in range(num_cols):
    temp_rows = find_peaks(-1 * padded_heights[:, col_ind])
    min_flag[temp_rows[0], col_ind] += 1

# our local minima should be places where we have min_flag == 2
local_minima = padded_heights[min_flag == 2]

# the risk level is the low point + 1
risk_minima = local_minima + 1

sum_risk = sum(risk_minima)
print("part 1 solution:", sum_risk)

# Part 2 wants us to find the size of areas bounded by 9s
basins = padded_heights.copy()

# convert all non edges of our basins to be equal to 1 so
# when we sum over all these values to get the area
basins[basins != 9] = 1

# convert the 9s to 0 to represent edges
basins[basins == 9] = 0

# we're going to use scipy.ndimages.measurements to find
# the basins. This function finds areas bounded by 0s and
# labels it as an element, exactly what we want
label, num_feature = measurements.label(
    basins
)

# now that we have areas labelled lets calculate the sums
basin_areas = measurements.sum(
    basins, label, index=np.arange(num_feature + 1)
)

# sort the basin areas in descending order
basin_areas[::-1].sort()

# get the product of the three biggest basins
prod_basin = int(np.product(basin_areas[:3]))

print("part 2 solution:", prod_basin)

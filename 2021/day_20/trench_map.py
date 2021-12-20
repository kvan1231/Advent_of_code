# https://adventofcode.com/2021/day/20


import numpy as np
from scipy.ndimage import convolve

# read in the input file
data = open("input.txt").read().splitlines()

# determine the algorithm from the data
algorithm = [
    pixel for pixel, point in enumerate(data[0]) if point == "#"
    ]

# pull out the image
image = np.pad(
    np.array(
        [[int(point == "#") for point in line] for line in data[2:]]
        ), ((50, 50), (50, 50))
)

# define the array for the rotation
rotation = np.array([[1, 2, 4], [8, 16, 32], [64, 128, 256]])

# count the number of lit pixels
for i in range(50):
    image = np.isin(
        convolve(image, rotation, mode="constant", cval=i % 2), algorithm
    ).astype(int)
    if i == 1:
        print("part 1:", image.sum())

print("part 2:", image.sum())

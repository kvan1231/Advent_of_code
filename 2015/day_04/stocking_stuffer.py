# https://adventofcode.com/2015/day/4

import hashlib
import itertools


def find_hash(input_file='input.txt', n=5):
    """
    Takes an input file name which contains a string. We take
    this string, which is the secret key, to find the MD5 hashes
    that starts with some number of zeroes. We return the lowest
    positive number that produces this hash when ignoring the
    leading zeros
    """

    # read in the input data
    input_data = open("input.txt").read().strip()

    # we need to endlessly iterate upwards from 1 until we
    # satisfy a condition
    for num in itertools.count(start=1):

        # create the hash string
        hash_str = input_data + str(num)

        # define the number of zeros we want to match
        matching_str = '0' * n

        # convert the hash string to md5
        md5_hash = hashlib.md5(hash_str.encode('utf-8')).hexdigest()[:n]

        # check if we found the number of leading zeros
        if md5_hash == matching_str:
            return(num)


print("Part 1: ", find_hash())
print("Part 2: ", find_hash(n=6))

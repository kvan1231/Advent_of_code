# https://adventofcode.com/2021/day/8

from itertools import permutations

# read in the input
file_name = "input.txt"
with open(file_name, 'r') as f:
    input_data = f.readlines()

# map the original digits combinations to specific numbers
orig_digits = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}

# find all permutations of the letters abcdefg
def_order = "abcdefg"
all_perms = [''.join(perm) for perm in permutations('abcdefg')]

# We want to count the number of 1, 4, 7 and 8
num_1478 = 0

# sum over all of the output values
summed_output = 0

# iterate through the rows in the input
for line in input_data:
    # split the line into the unique signal pattern (left)
    # and 4 digit output value (right)
    signal_pattern, output_val = line.split("|")
    signal_pattern_list = signal_pattern.split()
    output_val_list = output_val.strip().split()

    # 1, 4, 7 and 8 have outputs that are of length
    # 2, 3, 4, 7 respectively so lets check the length
    # of each digit in our output list
    for digit in output_val_list:
        if len(digit) in [2, 3, 4, 7]:
            num_1478 += 1

    # create a translator for a given permutation
    for perm_row in all_perms:
        translator = str.maketrans(def_order, "".join(perm_row))

        # create empty lists to store translated values
        trans_signal_list = []
        trans_digit = []

        # # translate the signal pattern
        for signal_digit in signal_pattern_list:
            translated_signal = signal_digit.translate(translator)
            trans_signal_list.append("".join(sorted(translated_signal)))

        # check if the translation reproduces the original digit combos
        if all(combo in orig_digits for combo in trans_signal_list):

            # translate the output using that translator
            for output_digit in output_val_list:
                translated_output = output_digit.translate(translator)
                sorted_output = "".join(sorted(translated_output))
                trans_digit.append(str(orig_digits[sorted_output]))

            # now convert the digit list into an actual number and add it
            combined_digit = int("".join(trans_digit))
            summed_output += combined_digit

            break


print("part 1 solution:", num_1478)
print("part 2 solution:", summed_output)
# https://adventofcode.com/2015/day/7


def input_data(input_file='input.txt'):
    """
    Read in an input file that contains input signals that produces outputs.
    We take this input file and converts it to a dictonary to be used.
    """
    input_dict = dict()

    with open(input_file) as f:
        raw_data = f.read().strip().split('\n')

    for row in raw_data:
        (signal, output) = row.split('->')
        input_dict[output.strip()] = signal.strip().split(' ')
    return input_dict


def circuit_value(key, input_dict, output_dict):
    """
    Takes a character and outputs the associated value of that character
    """
    # if the key is a number then just return the key as an int
    try:
        val = int(key)
        output_dict[key] = val
        return
    except ValueError:
        pass

    # get the dictionary entries we're interested in
    instructions = input_dict[key]

    # if theres only one entry on the side of the input
    # ex. 123 -> x
    if len(instructions) == 1:
        try:
            output_dict[key] = int(instructions[0])
        except ValueError:
            circuit_value(instructions[0], input_dict, output_dict)
            output_dict[key] = output_dict[instructions[0]]
    # if theres two entries on the input side, this only includes NOT entries
    # ex. NOT x -> h
    elif len(instructions) == 2:
        if instructions[0] == "NOT":
            char_key = instructions[1]

            # check to see if we already have the value
            if output_dict.get(char_key) is None:
                circuit_value(char_key, input_dict, output_dict)
            
            # time for bitwise complement of the value
            output_dict[key] = 0xffff - output_dict[char_key]

    # if there three entries on the input side
    elif len(instructions) == 3:
        # the four operators that can appear here are:
        #   AND, OR, RSHIFT, LSHIFT

        # split the instructions into left, right and operator
        left = instructions[0]
        operator = instructions[1]
        right = instructions[2]

        if output_dict.get(left) is None:
            circuit_value(left, input_dict, output_dict)
        if output_dict.get(right) is None:
            circuit_value(right, input_dict, output_dict)

        # check what operator we have
        if operator == "AND":
            output_dict[key] = output_dict[left] & output_dict[right]
        if operator == "OR":
            output_dict[key] = output_dict[left] | output_dict[right]
        if operator == "RSHIFT":
            output_dict[key] = 0xffff & (output_dict[left] >> int(right))
        if operator == "LSHIFT":
            output_dict[key] = 0xffff & (output_dict[left] << int(right))


def sol_pipeline(key='a'):
    input_dict = input_data('input.txt')
    output_dict = {}
    circuit_value(key, input_dict, output_dict)
    print("Part 1: ", output_dict[key])

    input_dict2 = input_data('input2.txt')
    output_dict2 = {}
    circuit_value(key, input_dict2, output_dict2)
    print("Part 2: ", output_dict2[key])

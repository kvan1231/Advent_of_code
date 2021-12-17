# https://adventofcode.com/2021/day/16

from functools import reduce
from operator import mul


def convert_to_bit(hex_data):
    """
    Python can effectively translate numbers from
    one base to another, this function will convert
    a hexadecimal to bits and pad it with zeros
    """

    decimal_form = int(hex_data, 16)

    # drop the first two characters so we just keep the bits
    bit_form = bin(decimal_form)[2:]

    # check to see if we need padding
    len_bits = len(bit_form)
    if len_bits % 4 > 0:
        padding_zeros = "0" * (4 - len_bits % 4)
        bit_form = padding_zeros + bit_form

    return bit_form


def translate_packet(bit_form):
    """
    The first 3 bits are the version, the next 3 bits are
    the type id, the following bits are can be sub packets
    """
    packet = {
        "version": int(bit_form[0:3], 2),
        "type_id": int(bit_form[3:6], 2),
        "sub_packet": []
    }
    # print("version", packet["version"])
    # print("type id", packet["type_id"])

    # if the type_id == 4 then the packet represents a literal value
    if packet["type_id"] == 4:
        remaining_bits = bit_form[6:]

        # if we're on the last set of bits the first digit is 0
        # we're going to set this flag to True until we encounter
        # this last set
        not_last = True

        # initialize the variable to hold the bn
        binary_val = ""
        while not_last:
            # check if we're at the last set of bits
            not_last = remaining_bits[0] != "0"

            # grab the set of bits
            bit_set = remaining_bits[1:5]

            # slice the remaining bits
            remaining_bits = remaining_bits[5:]

            # add the bits to the string
            binary_val = binary_val + bit_set
        packet["value"] = int(binary_val, 2)
        return packet, remaining_bits

    return translate_sub_packet(bit_form, packet)


def translate_sub_packet(bits, packet):
    """
    This function now moves through the sub-packets in the data
    """

    # print("sub packet")

    # the length type ID is the first bit following the
    # version and type ID if the type ID wasn't 4
    length_type_id = bits[6]

    # print("length type id", length_type_id)

    # if the length type id is 0
    if length_type_id == "0":
        # the next 15 bits are a number that represents the total
        # length in bits
        total_length = int(bits[7:22], 2)
        sub_bits = bits[22:22 + total_length]
        remaining_bits = bits[22 + total_length:]
        while len(sub_bits):
            sub_packet, sub_bits = translate_packet(sub_bits)
            packet["sub_packet"].append(sub_packet)

    # if the length type id is 1
    else:
        # the next 11 bits are a number that represents the number
        # of sub-packets contained
        num_sub_packets = int(bits[7:18], 2)
        remaining_bits = bits[18:]
        for packet_num in range(num_sub_packets):
            sub_packet, remaining_bits = translate_packet(remaining_bits)
            packet["sub_packet"].append(sub_packet)
    return packet, remaining_bits


def calc_version_sum(packet):
    sum_sub_packets = sum(
        calc_version_sum(sub_packet) for sub_packet in packet["sub_packet"]
    )
    version_sum = packet["version"] + sum_sub_packets
    # print(packet["sub_packet"])
    return version_sum


def calc_value(packet):
    """
    In part 2, depending on the type ID there are different
    ways to calculate the output value
    """

    # if the type id is 0 then sum the packet
    if packet["type_id"] == 0:
        return sum(
            calc_value(sub_packet) for sub_packet in packet["sub_packet"]
        )

    # if the type id is 1 then multiply
    if packet["type_id"] == 1:
        # easiest way to multiply the nested packet we need to use the reduce
        # function and the mul function
        return reduce(
            mul, (
                calc_value(sub_packet) for sub_packet in packet["sub_packet"]
            ), 1
        )

    # if the type id is 2 then return the minimum value in the sub packets
    if packet["type_id"] == 2:
        return min(
            calc_value(sub_packet) for sub_packet in packet["sub_packet"]
        )

    # if the type id is 3 then return the maximum value in the sub packets
    if packet["type_id"] == 3:
        return max(
            calc_value(sub_packet) for sub_packet in packet["sub_packet"]
        )

    # if the type id is 4 then return the literal value
    if packet["type_id"] == 4:
        return packet["value"]

    # if the type id is 5 then return 1 if the first sub packet is greater than
    # the second sub packet
    if packet["type_id"] == 5:
        first_sub_packet = calc_value(packet["sub_packet"][0])
        second_sub_packet = calc_value(packet["sub_packet"][1])
        return int(first_sub_packet > second_sub_packet)

    # if the type id is 6 then return 1 if the first sub packet is less than
    # the second sub packet
    if packet["type_id"] == 6:
        first_sub_packet = calc_value(packet["sub_packet"][0])
        second_sub_packet = calc_value(packet["sub_packet"][1])
        return int(first_sub_packet < second_sub_packet)

    # if the type id is 7 then return 1 if the first sub packet is equal to
    # the second sub packet
    if packet["type_id"] == 7:
        first_sub_packet = calc_value(packet["sub_packet"][0])
        second_sub_packet = calc_value(packet["sub_packet"][1])
        return int(first_sub_packet == second_sub_packet)


def p1_bit_pipeline(input_file):
    hex_data = open(input_file).read().strip()

    # print("converting it to bits")
    bits = convert_to_bit(hex_data)

    # print("generating the packet tree")
    packet, _ = translate_packet(bits)

    ver_sum = calc_version_sum(packet)
    return ver_sum


def p2_bit_pipeline(input_file):
    hex_data = open(input_file).read().strip()

    # print("converting it to bits")
    bits = convert_to_bit(hex_data)

    # print("generating the packet tree")
    packet, _ = translate_packet(bits)

    value = calc_value(packet)
    return value


def tests():

    # read in the data
    p1_input_files = [
        "test_1.txt",
        "test_2.txt",
        "test_3.txt",
        "test_4.txt"
    ]

    p2_input_files = [
        "test_5.txt",
        # "test_6.txt",
        "test_7.txt",
        "test_8.txt",
        "test_9.txt",
        "test_10.txt",
        "test_11.txt",
        "test_12.txt"
    ]

    for input_file in p1_input_files:
        p1_sum = p1_bit_pipeline(input_file)
        print(input_file, p1_sum)

    for input_file in p2_input_files:

        p2_value = p2_bit_pipeline(input_file)
        print(input_file, p2_value)


p1_sol = p1_bit_pipeline("input.txt")
print("part 1 solution:", p1_sol)

p2_sol = p2_bit_pipeline("input.txt")
print("part 2 solution:", p2_sol)

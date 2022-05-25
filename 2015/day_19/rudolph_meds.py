# https://adventofcode.com/2015/day/19

import re


def read_data(input_file='input.txt'):
    """
    Reads in an input file that contains character conversions and
    the string of characters representing a molecule to be converted
    """

    # read in the file
    with open(input_file, 'r') as f:
        raw_data = f.read()

    # split the data into a list
    raw_list = raw_data.split('\n')
    # remove any empty elements
    clean_list = list(filter(None, raw_list))

    # initialize the replacement list
    replacements = []

    # The last entry in the list is the molecule to be converted
    molecule = clean_list[-1]

    # loop through the other entries
    for replacement in clean_list[:-1]:

        # use some real expressions to grab the replacements
        re_pair = re.findall(r'(\S+) => (\S+)', replacement)

        # append to our list of replacements
        replacements.append(re_pair[0])

    return replacements, molecule


def gen_molecules(molecule, replacements):
    """
    Takes an inputted molecule that is a string of characters and iterates
    through the list of replacements to generate a set of possible molecules
    """

    # initialize the set
    molecule_set = set()

    # loop and replace
    # grab the initial character chunk and replacement chunk
    for init, repl in replacements:
        # step through the molecule
        for mol_ind in range(len(molecule)):
            # define the sub molecule as the section of the molecule
            # that has the same length as our initial character chunk
            # we want to replace
            sub_molecule = molecule[mol_ind:mol_ind+len(init)]

            # if the sub molecule is the same as our initial chunk
            if sub_molecule == init:

                # generate the new molecule
                molecule_left = molecule[:mol_ind]
                molecule_right = molecule[mol_ind + len(init):]
                changed_molecule = molecule_left + repl + molecule_right

                # add that new molecule to the set
                molecule_set.add(changed_molecule)

    # output the molecule set
    return molecule_set


def fab_molecule(molecule, replacements):
    """
    Determines the fewest number of replacements necessary to generate
    the target molecule from a single starting electron e
    """
    # initialize the number of replacements needed to be made
    num_replacements = 0

    # define our target molecule
    target_mol = molecule

    # make a copy of the replacements list
    temp_repl = replacements.copy()

    # we're going to work backwards from our target molecule
    # loop until our molecule doesnt equal electron
    while target_mol != 'e':
        # there are cases where we will run out of pairs to replace
        try:
            # find the longest molecule chunk the replacement list
            long_chunk = max(temp_repl, key=lambda pair: len(pair[1]))
        # in that case, regenerate the list
        except ValueError:
            temp_repl = replacements.copy()
            # find the longest molecule chunk the replacement list
            long_chunk = max(temp_repl, key=lambda pair: len(pair[1]))

        # split into init and replacement
        init, repl = long_chunk

        # perform the replacement
        new_mol = target_mol.replace(repl, init, 1)

        # iterate and remove replacements
        if target_mol != new_mol:
            num_replacements += 1
        else:
            temp_repl.remove(long_chunk)
        target_mol = new_mol

    return num_replacements


def sol_pipeline(input_file='input.txt'):
    """
    Quick command to generate the solutions
    """

    repl, mole = read_data(input_file)
    p1_set = gen_molecules(mole, repl)
    p1_sol = len(p1_set)
    print("P1 Solution:", p1_sol)

    p2_sol = fab_molecule(mole, repl)
    print("P1 Solution:", p2_sol)

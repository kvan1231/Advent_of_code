# https://adventofcode.com/2021/day/23


def return_board(board='p1_test'):
    """
    Read in the amphipod map and returns it. I couldn't come up
    with a good way to pull useful data out of the text input.
    We're going to manually format the data so that it goes from

    #############
    #...........#
    ###B#C#B#D###
      #A#D#C#A#
      #########

    to

    .. . . . ..
      B C B D
      A D C A

    and will be output as a list in the form
    ['.', '.', 'BA', '.', 'CD', '.', 'BC', '.', 'DA', '.', '.']

    """
    if board == 'p1_test':
        init_board = [
            '.', '.', 'BA', '.', 'CD', '.', 'BC', '.', 'DA', '.', '.'
        ]
        final_board = [
                '.', '.', 'AA', '.', 'BB', '.', 'CC', '.', 'DD', '.', '.'
        ]
    elif board == 'p1_input':
        init_board = [
            '.', '.', 'DC', '.', 'CD', '.', 'AA', '.', 'BB', '.', '.'
        ]
        final_board = [
                '.', '.', 'AA', '.', 'BB', '.', 'CC', '.', 'DD', '.', '.'
        ]
    elif board == 'p2_test':
        init_board = [
            '.', '.', 'BDDA', '.', 'CCBD', '.', 'BBAC', '.', 'DACA', '.', '.'
        ]
        final_board = [
                '.', '.', 'AAAA', '.', 'BBBB',
                '.', 'CCCC', '.', 'DDDD', '.', '.'
        ]
    elif board == 'p2_input':
        init_board = [
            '.', '.', 'DDDC', '.', 'CCBD', '.', 'ABAA', '.', 'BACB', '.', '.'
        ]
        final_board = [
                '.', '.', 'AAAA', '.', 'BBBB',
                '.', 'CCCC', '.', 'DDDD', '.', '.'
        ]

    return init_board, final_board


def sim_move(board):
    """
    This function simulates the movements of the amphipods to different
    positions and calculates the lowest cost necessary to reach this state.
    This function returns all of these different states along with the
    associated minimum cost.
    """

    # create a dictonary of the possible boards and the costs
    possible_states = {tuple(board): 0}

    # convert the board into a list that we'll loop through
    board_list = [board]

    # looping through the list
    while board_list:
        # print(len(board_list))
        temp_board = board_list.pop()
        for position, item in enumerate(temp_board):
            # print(position, item)
            # check if the item in the position is an amphipod
            if _move_from_pos(item) is None:
                continue
            destinations = move_permutations(temp_board, position)

            for temp_dest in destinations:
                new_board, new_cost = move_item(
                    temp_board, position, temp_dest
                )
                rolling_cost = possible_states[tuple(temp_board)] + new_cost
                new_board_tuple = tuple(new_board)
                cost = possible_states.get(new_board_tuple, 9999999)
                if rolling_cost < cost:
                    possible_states[new_board_tuple] = rolling_cost
                    board_list.append(new_board)

    return possible_states


def move_item(board, position, destination):
    """
    This function takes a board, moves an item from a position to a
    destination then returns the updated board along with the cost
    of making this move.
    """
    cost = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    new_board = board.copy()
    distance = 0
    move_amphi = _move_from_pos(board[position])

    # check if the boards position is a hall or a room with 2 spots
    if len(board[position]) == 1:
        new_board[position] = '.'

    else:
        new_loc = ''
        found_loc = False
        for item in board[position]:
            if item == '.':
                distance += 1
                new_loc += item
            elif not found_loc:
                new_loc += '.'
                distance += 1
                found_loc = True
            else:
                new_loc += item
        new_board[position] = new_loc

    distance += abs(position - destination)

    if len(board[destination]) == 1:
        new_board[destination] = move_amphi
        return new_board, distance * cost[move_amphi]
    else:
        new_board[destination], add_dist = _go_into_pos(
            move_amphi, board[destination]
        )
        distance += add_dist
        return new_board, distance * cost[move_amphi]


def move_permutations(board, position):
    """
    This function generates all possible moves an amphipod can perform
    on a given board
    """

    # create a dictonary of where the final positons of the amphipods
    final_dict = {
        'A': 2,
        'B': 4,
        'C': 6,
        'D': 8
    }
    # keep only the locations
    final_positions = set(final_dict.values())

    # get the amphipod
    amphipod = board[position]

    # print(board, position, amphipod)
    # if the position we're interested in isnt it's final spot
    if position not in final_positions:
        # print("chk 1")
        # is the path blocked
        move_chk = _can_move(
            board, position, final_dict[amphipod], final_positions
        )
        # is there room at the destination
        room_chk = _check_in_location(
            board, final_dict[amphipod], amphipod
        )
        if move_chk and room_chk:
            # print("chk 2")
            return [final_dict[amphipod]]
        return []

    # grab the amphipod to move
    move_amphi = _move_from_pos(amphipod)

    # is there room at the position
    room_chk = _check_in_location(
        board, position, move_amphi
    )
    # the amphipod is already where it wants to be
    if position == final_dict[move_amphi] and room_chk:
        # print("chk 3")
        return []

    # create a list of possible moves
    possible_moves = []

    # lets now loop through the other destinations
    for destinations in range(len(board)):
        # if the destination is the position provided then continue
        if destinations == position:
            # print("chk 4")
            continue

        # if the destination is a final space but not the goal
        # of the amphipod we're looking at then continue
        fp_chk = destinations in final_positions
        amphi_goal_chk = final_dict[move_amphi] != destinations
        if fp_chk and amphi_goal_chk:
            # print("chk 5")
            continue

        # if we're moving the amphipod to its final destination
        # but there's no room
        room_chk = _check_in_location(
            board, destinations, move_amphi
        )
        if (not amphi_goal_chk) and (not room_chk):
            # print("chk 6")
            continue

        # if the path is clear
        move_chk = _can_move(
            board, position, destinations, final_positions
        )
        if move_chk:
            # print("chk 7")
            possible_moves.append(destinations)
    return possible_moves


def _move_from_pos(item):
    """
    This function checks if an amphipod, if it is then return the amphipod,
    otherwise reteun nothing
    """
    for sub_item in item:
        if sub_item != '.':
            return sub_item


def _go_into_pos(amphi, pos):
    """
    This function adds an amphipod to the position
    """
    pos_list = list(pos)
    vacancy = pos_list.count('.')

    # effectively doing if vacancy not != 0
    assert vacancy != 0
    pos_list[vacancy - 1] = amphi

    return ''.join(pos_list), vacancy


def _can_move(board, position, destination, final_positions):
    """
    Checks to see if its possible for a piece in a board at a given position
    can reach a destination point. All positions between the leftmost and
    rightmost position must be '.' or the move is not possible.
    """

    # find the leftmost and rightmost positions
    leftmost = min(position, destination)
    rightmost = max(position, destination)

    # loop through the positions between the left and rightmost positions
    for pos in range(leftmost, rightmost + 1):
        # continue if the position matches the starting position
        if pos == position:
            continue
        # continue if the position matches with a final destination
        if pos in final_positions:
            continue
        # we encounter another amphipod along the path then return False
        if board[pos] != '.':
            return False

    return True


def _check_in_location(board, location, amphi):
    """
    This function checks a location on the board to see if that location
    is either empty, partially empty with the appropriate amphipod or is
    filled with the correct amphipods.
    """

    board_loc = board[location]

    # determine the max number of spots in that location
    board_occupancy = len(board_loc)

    # count the number of vacancies at that spot
    empty_count = board_loc.count('.')

    # count the number of amphipods that are supposed to be there
    amphi_count = board_loc.count(amphi)

    return board_occupancy == empty_count + amphi_count


def sol_pipeline():
    """
    Run this function to spit out the two tests and two input solutions
    """

    p1_init_test, p1_final_test = return_board(board='p1_test')
    p1_test_states = sim_move(p1_init_test)
    p1_test = p1_test_states[tuple(p1_final_test)]

    p1_init_input, p1_final_input = return_board(board='p1_input')
    p1_input_states = sim_move(p1_init_input)
    p1_sol = p1_input_states[tuple(p1_final_input)]

    p2_init_test, p2_final_test = return_board(board='p2_test')
    p2_test_states = sim_move(p2_init_test)
    p2_test = p2_test_states[tuple(p2_final_test)]

    p2_init_input, p2_final_input = return_board(board='p2_input')
    p2_input_states = sim_move(p2_init_input)
    p2_sol = p2_input_states[tuple(p2_final_input)]

    print("Tests")
    print("=====")
    print("Part 1: ", p1_test)
    print("Part 2: ", p2_test)

    print("\nResults")
    print("=======")
    print("Part 1: ", p1_sol)
    print("Part 2: ", p2_sol)

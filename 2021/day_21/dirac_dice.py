# https://adventofcode.com/2021/day/21

from collections import defaultdict
from collections import Counter


def read_data(input_file='test.txt'):
    """
    Read in the raw data, strip away the strings and return the
    initial positions
    """

    raw_data = open(input_file).read().strip().split('\n')
    init_pos = [int(line.split(": ")[-1]) for line in raw_data]
    return init_pos


def increment_sim(init_pos):
    """
    This function takes in a list of two initial positions and
    simulates a game of dirac dice. Each step a dice will increment
    up by 3 and the scores of each player will increase by the
    position the player ends the turn on. This game ends when
    a players score reaches or exceeds 1000.
    """

    # initialize the player positions and scores
    player_pos = init_pos.copy()
    player_scores = [0, 0]

    # initialize the initial dice score
    dice_val = 1

    while True:
        # print("player positions: ", player_pos)
        # print("player scores: ", player_scores)

        # loop through the two players
        for player in range(2):

            # print(dice_pos)
            # calculate the chanage in position
            pos_change = sum(range(dice_val, dice_val+3))

            # the positon loops around AFTER we pass by 10
            temp_pos = (player_pos[player] + pos_change - 1) % 10 + 1
            # print(temp_pos)

            # update the player position and scores
            player_pos[player] = temp_pos
            player_scores[player] += temp_pos

            # update the dice
            dice_val += 3

            # if either of the players scores exceed 1000
            if player_scores[player] >= 1000:

                # return the losing players score and number of dice rolls
                losing_score = player_scores[player - 1]
                dice_rolls = dice_val - 1
                return losing_score, dice_rolls


def quantum_sim(init_pos):
    """
    Now instead of a dice that constantly increments, the dice only has
    3 sides and each time we roll the dice we split into multiple versions
    for each possible solution. The game progresses the same as increment_sim
    but instead ends when a player reaches 21 points or greater. This function
    simulates this game and then returns the number of possible outcomes where
    the player who wins more often.
    """

    # grab the initial positions
    p1_init, p2_init = init_pos.copy()

    # generate all dice combinations and the counts
    dice_combo = list(Counter(
        d1 + d2 + d3
        for d1 in range(1, 4)
        for d2 in range(1, 4)
        for d3 in range(1, 4)
    ).items())

    # initialize the universe
    universe = {(0, p1_init, 0, p2_init): 1}

    # create the variables to count number of wins
    p1_wins = 0
    p2_wins = 0
    while universe:
        new_universe = defaultdict(int)
        for universe_state, count in list(universe.items()):

            # pull out the scores and position of the universe
            p1_score, p1_pos, p2_score, p2_pos = universe_state

            # for a specific dice configuration used for p1
            for d1_val, d1_count in dice_combo:
                # update position and score
                p1_new_pos = (p1_pos + d1_val - 1) % 10 + 1
                p1_new_score = p1_score + p1_new_pos

                # if p1 score exceeds 21
                if p1_new_score >= 21:

                    # add the number of common universes
                    # and common dice states to p1 wins
                    p1_wins += count * d1_count
                    continue

                # now to loop through dice for p2
                for d2_val, d2_count in dice_combo:
                    # update position and score
                    p2_new_pos = (p2_pos + d2_val - 1) % 10 + 1
                    p2_new_score = p2_score + p2_new_pos

                    # if p2 score exceeds 21
                    if p2_new_score >= 21:

                        # add the number of common universes
                        # and common dice states to p1 wins
                        p2_wins += count * d1_count * d2_count
                        continue
                    # update the universe
                    new_universe[(
                        p1_new_score, p1_new_pos, p2_new_score, p2_new_pos
                        )] += count * d1_count * d2_count
        # replace the old universe with the new universe
        universe = new_universe

    # return the number of wins
    return p1_wins, p2_wins


def sim_pipeline(input_file):
    init_pos = read_data(input_file)

    losing_score, dice_rolls = increment_sim(init_pos)
    part1_sol = losing_score * dice_rolls

    p1_wins, p2_wins = quantum_sim(init_pos)
    part2_sol = max([p1_wins, p2_wins])

    print("part 1:", part1_sol)
    print("part 2:", part2_sol)


sim_pipeline('test.txt')
sim_pipeline('input.txt')

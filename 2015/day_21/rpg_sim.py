# https://adventofcode.com/2015/day/21

import itertools


def read_items(input_file="items.txt"):
    """
    Reads in a file containing the names and properties of various rpg
    items and returns the data as three lists
    """

    # initialize the lists containing the properties
    weaps = []
    armor = []
    rings = []

    # we must always choose a weapon but we dont need amor or rings,
    # use rows with 0s to denote no armor or rings
    armor.append([0, 0, 0])
    rings.append([0, 0, 0])
    rings.append([0, 0, 0])

    # create the list of categories
    categ = ["weapons", "armor", "rings"]
    cat_ind = -1

    # read in the file
    with open(input_file, 'r') as f:
        raw_data = f.read()

    # split the data into a list
    raw_list = raw_data.split('\n')
    # remove any empty elements
    clean_list = list(filter(None, raw_list))

    # loop through the rows
    for item_ind in range(len(clean_list)):

        # check what category it is
        category = categ[cat_ind]
        # grab the item
        item = clean_list[item_ind]
        # if the row is a header row then just iterate our category value
        if 'Cost' in item:
            cat_ind += 1
            continue
        # if it isnt a header row then append the information to the right
        # table
        else:
            # split and convert the properties to integers
            item_props = item.split()[-3:]
            item_vals = list(map(int, item_props))
            if category == "weapons":
                weaps.append(item_vals)
            if category == "armor":
                armor.append(item_vals)
            if category == "rings":
                rings.append(item_vals)

    return weaps, armor, rings


def read_stats(input_file='input.txt'):
    """
    Read in the enemys stats and output them as a list of ints
    """

    # read in the file
    with open(input_file, 'r') as f:
        raw_data = f.read()

    raw_list = raw_data.split('\n')

    enemy_stats = [int(row.split(":")[1]) for row in raw_list]

    return enemy_stats


def combat_sim(player_stats, enemy_stats):
    """
    Determines the winner in combat depending on the stats of the
    player and enemy
    """
    enemy_hp, enemy_dmg, enemy_armor = enemy_stats
    player_hp, player_dmg, player_armor = player_stats

    while True:
        enemy_hp -= max(player_dmg - enemy_armor, 1)
        if enemy_hp <= 0:
            return True
        player_hp -= max(enemy_dmg - player_armor, 1)
        if player_hp <= 0:
            return False


def gold_cost():
    """
    Calculates the amount of gold spent on items and returns the
    amount of gold that results in a win
    """

    weapons, armor, rings = read_items()
    enemy_stats = read_stats()

    win_cost = []
    loss_cost = []

    for weap_cost, weap_dmg, _ in weapons:
        for armor_cost, _, armor_armor in armor:
            for ring1, ring2 in itertools.combinations(rings, 2):
                ring1_cost, ring1_dmg, ring1_armor = ring1
                ring2_cost, ring2_dmg, ring2_armor = ring2

                tot_dmg = weap_dmg + ring1_dmg + ring2_dmg
                tot_armor = armor_armor + ring1_armor + ring2_armor
                total_cost = weap_cost + armor_cost + ring1_cost + ring2_cost

                player_stats = [100, tot_dmg, tot_armor]

                if combat_sim(player_stats, enemy_stats):
                    win_cost.append(total_cost)

                elif not combat_sim(player_stats, enemy_stats):
                    loss_cost.append(total_cost)

    return min(win_cost), max(loss_cost)


def sol_pipeline():
    """
    Quick and dirty pipeline to print the solutions
    """

    p1_cost, p2_cost = gold_cost()
    print("P1 Solution:", p1_cost)
    print("P2 Solution:", p2_cost)

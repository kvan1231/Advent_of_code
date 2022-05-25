# https://adventofcode.com/2015/day/21

import pandas as pd


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


def gen_spells():
    """
    Returns the list of spells that can be used
    """

    magic_missile = ['magic_missile', 53, 4, 0, 0, 0, 0]
    drain = ['drain', 72, 2, 4, 0, 0, 0]
    shield = ['shield', 113, 0, 0, 7, 0, 6]
    poison = ['poison', 173, 3, 0, 0, 0, 6]
    recharge = ['recharge', 228, 0, 0, 0, 101, 5]

    spell_list = [magic_missile, drain, shield, poison, recharge]

    spell_df = pd.DataFrame(spell_list, columns=[
        'spell', 'cost', 'dmg', 'hp', 'armor', 'regen', 'turns'
    ])

    return spell_df.set_index('spell')


def combat_sim(actions, part):
    """
    Determines the winner in combat depending on the stats of the
    player and enemy
    """

    # initialize all the values
    enemy_hp, enemy_dmg = read_stats()
    player_hp, player_mana, player_armor = 50, 500, 0

    # turn counts
    turn_count, temp_turns = 0, 0

    # create a turn tracker to determine whos turn it is
    # if 1 then player turn
    # if -1 then enemy turn
    whos_turn = 1

    # keep track of mana spent
    mana_spent = 0

    # keep track of poison, shield and recharge turns
    p_turns, s_turns, r_turns = 0, 0, 0

    # generate the spell information
    spells = gen_spells()

    # spell dictionary
    spell_dict = {
        'M': 'magic_missile',
        'D': 'drain',
        'S': 'shield',
        'P': 'poison',
        'R': 'recharge'
    }

    # start the loop
    while True:
        # check if poison is active
        if p_turns:
            p_turns = max(p_turns - 1, 0)
            enemy_hp -= spells.loc['poison'].dmg

        # check if shield is active
        if s_turns:
            s_turns = max(s_turns - 1, 0)
            player_armor = spells.loc['shield'].armor
        else:
            player_armor = 0

        # check if recharge is active
        if r_turns:
            r_turns = max(r_turns - 1, 0)
            player_mana += spells.loc['recharge'].regen

        # if its player turn
        if whos_turn == 1:
            if part == 2:
                player_hp -= 1
                if player_hp <= 0:
                    return 0
            # grab a spell
            spell = spell_dict[actions[temp_turns]]
            # apply the cost
            player_mana -= spells.loc[spell].cost
            mana_spent += spells.loc[spell].cost

            # apply the damage and hp from spells
            enemy_hp -= spells.loc[spell].dmg
            player_hp += spells.loc[spell].hp

            # if we cast shield, poison or recharge then apply number effects
            if spell == 'shield':
                if s_turns:
                    return 0
                s_turns = 6
            elif spell == 'poison':
                if p_turns:
                    return 0
                p_turns = 6
            elif spell == 'recharge':
                if r_turns:
                    return 0
                r_turns = 5

            # if we're out of mana
            if player_mana < 0:
                return 0

        # if the enemy has 0 hp
        if enemy_hp <= 0:
            return mana_spent

        # if its the enemys turn
        if whos_turn == -1:
            # take some damage
            player_hp -= max(enemy_dmg - player_armor, 1)

            # if we're out of hp
            if player_hp <= 0:
                return 0

        # flip whos turn it is
        if whos_turn == 1:
            temp_turns += 1

        whos_turn = -whos_turn
        turn_count += 1


def iterate_actions(pos):
    actions[pos] = 'DSPRM'['MDSPR'.index(actions[pos])]
    if actions[pos] == 'M':
        if pos+1 <= len(actions):
            iterate_actions(pos+1)


for part in (1, 2):
    actions = ['M'] * 20
    min_spent = 1000000
    for i in range(1000000):
        result = combat_sim(actions, part)
        if result:
            min_spent = min(result, min_spent)
        iterate_actions(0)
    print(min_spent)

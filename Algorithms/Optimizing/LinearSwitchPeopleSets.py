import itertools
import math

from Utils.UtilFunctions import getAllPeople
from Utils.ValueCalc import calcTable


def _score_affected_tables(arrangement, affected_tables):
    calc_table = calcTable
    total = 0
    for table_index in affected_tables:
        total += calc_table(arrangement[table_index])[0]
    return total


def _apply_switch(arrangement, permutation):
    first_table_index, first_seat_index = permutation[0]
    first_value = arrangement[first_table_index][first_seat_index]

    for index in range(len(permutation) - 1):
        current_table_index, current_seat_index = permutation[index]
        next_table_index, next_seat_index = permutation[index + 1]
        arrangement[current_table_index][current_seat_index] = arrangement[next_table_index][next_seat_index]

    last_table_index, last_seat_index = permutation[-1]
    arrangement[last_table_index][last_seat_index] = first_value


def _revert_switch(arrangement, permutation):
    last_table_index, last_seat_index = permutation[-1]
    last_value = arrangement[last_table_index][last_seat_index]

    for index in range(len(permutation) - 1, 0, -1):
        current_table_index, current_seat_index = permutation[index]
        previous_table_index, previous_seat_index = permutation[index - 1]
        arrangement[current_table_index][current_seat_index] = arrangement[previous_table_index][previous_seat_index]

    first_table_index, first_seat_index = permutation[0]
    arrangement[first_table_index][first_seat_index] = last_value


def _run_switch_size(arrangement, switch_size, coords, verbose):
    iterator = itertools.combinations(coords, 2) if switch_size == 2 else itertools.permutations(coords, switch_size)
    apply_switch = _apply_switch
    revert_switch = _revert_switch
    score_affected_tables = _score_affected_tables

    coord_count = len(coords)
    iter_len = math.comb(coord_count, 2) if switch_size == 2 else math.perm(coord_count, switch_size)
    if verbose:
        print(f"Amount of iterations for {switch_size}: {iter_len}")

    progress_interval = iter_len // 10 if switch_size > 2 and iter_len >= 10 else 0

    counter = 0
    for permutation in iterator:
        affected_tables = {table_index for table_index, _ in permutation}
        pre_value_total = score_affected_tables(arrangement, affected_tables)

        apply_switch(arrangement, permutation)
        post_value_total = score_affected_tables(arrangement, affected_tables)

        if post_value_total < pre_value_total:
            revert_switch(arrangement, permutation)

        if verbose:
            counter += 1
            if progress_interval and counter % progress_interval == 0:
                print(f"Progress for switch size {switch_size}: {counter}/{iter_len} ({(counter / iter_len) * 100:.2f}%)")

def LinearSwitchPeopleSets(arrangement, v, coords=None, verbose = False):
    if v < 2:
        raise ValueError("v must be greater than or equal to 2")

    if coords is None:
        coords = getAllPeople(arrangement)

    for switch_size in range(2, v + 1):
        _run_switch_size(arrangement, switch_size, coords, verbose)

    return arrangement


def linearSwitchPeopleEachTable(initialArrangement, v):
    best_arrangement = []

    for table in initialArrangement:
        optimized_single_table = LinearSwitchPeopleSets([list(table)], v)
        best_arrangement.append(optimized_single_table[0])

    return best_arrangement


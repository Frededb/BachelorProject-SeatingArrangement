import itertools

from Utils.UtilFunctions import getAllPeople
from Utils.ValueCalc import calcTable


def _score_affected_tables(arrangement, permutation):
    affected_tables = {person[0] for person in permutation}
    return sum(calcTable(arrangement[table_index])[0] for table_index in affected_tables)


def _apply_switch(arrangement, permutation):
    values = [arrangement[table_index][seat_index] for table_index, seat_index in permutation]
    rotated = values[1:] + values[:1]
    for (table_index, seat_index), value in zip(permutation, rotated):
        arrangement[table_index][seat_index] = value


def _revert_switch(arrangement, permutation):
    values = [arrangement[table_index][seat_index] for table_index, seat_index in permutation]
    rotated_back = values[-1:] + values[:-1]
    for (table_index, seat_index), value in zip(permutation, rotated_back):
        arrangement[table_index][seat_index] = value


def _run_switch_size(arrangement, switch_size, coords):
    iterator = itertools.combinations(coords, 2) if switch_size == 2 else itertools.permutations(coords, switch_size)

    for permutation in iterator:
        pre_value_total = _score_affected_tables(arrangement, permutation)
        _apply_switch(arrangement, permutation)
        post_value_total = _score_affected_tables(arrangement, permutation)

        if post_value_total < pre_value_total:
            _revert_switch(arrangement, permutation)


def LinearSwitchPeopleSets(arrangement, v, coords=None):
    if v < 1:
        raise ValueError("v must be greater than 1")

    if coords is None:
        coords = getAllPeople(arrangement)

    for switch_size in range(2, v + 1):
        _run_switch_size(arrangement, switch_size, coords)

    return arrangement


def linearSwitchPeopleEachTable(initialArrangement, v):
    best_arrangement = []

    for table in initialArrangement:
        optimized_single_table = LinearSwitchPeopleSets([list(table)], v)
        best_arrangement.append(optimized_single_table[0])

    return best_arrangement


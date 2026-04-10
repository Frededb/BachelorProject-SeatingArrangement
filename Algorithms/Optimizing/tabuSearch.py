import random
from copy import deepcopy

from Utils.UtilFunctions import getAllPeople, switch
from Utils.ValueCalc import calcArrangement, calcTable


def _move_key(person_a, person_b):
    return (person_a, person_b) if person_a <= person_b else (person_b, person_a)


def _score_after_swap(arrangement, current_score, person_a, person_b):
    table_a, table_b = person_a[0], person_b[0]

    if table_a == table_b:
        before = calcTable(arrangement[table_a])[0]
        switch(arrangement, person_a, person_b)
        after = calcTable(arrangement[table_a])[0]
        switch(arrangement, person_a, person_b)
        return current_score - before + after

    before_a = calcTable(arrangement[table_a])[0]
    before_b = calcTable(arrangement[table_b])[0]
    switch(arrangement, person_a, person_b)
    after_a = calcTable(arrangement[table_a])[0]
    after_b = calcTable(arrangement[table_b])[0]
    switch(arrangement, person_a, person_b)
    return current_score - before_a - before_b + after_a + after_b


def _sample_pairs(rng, seat_indices, neighborhood_size):
    seat_count = len(seat_indices)
    max_pairs = seat_count * (seat_count - 1) // 2
    sample_count = min(neighborhood_size, max_pairs)

    if sample_count <= 0:
        return []

    if sample_count == max_pairs and max_pairs <= 5000:
        pairs = []
        for i in range(seat_count):
            for j in range(i + 1, seat_count):
                pairs.append((seat_indices[i], seat_indices[j]))
        return pairs

    seen = set()
    pairs = []
    while len(pairs) < sample_count:
        i, j = rng.sample(range(seat_count), 2)
        if i > j:
            i, j = j, i
        if (i, j) in seen:
            continue
        seen.add((i, j))
        pairs.append((seat_indices[i], seat_indices[j]))
    return pairs


def tabuSearch(
    arrangement,
    iterations=1500,
    tabu_tenure=30,
    neighborhood_size=120,
    max_no_improve=300,
    seed=None,
):
    rng = random.Random(seed)
    seat_indices = getAllPeople(arrangement)

    if len(seat_indices) < 2:
        return arrangement

    current_score = calcArrangement(arrangement)[0]
    best_score = current_score
    best_arrangement = deepcopy(arrangement)

    tabu_until = {}
    no_improve = 0

    for iteration in range(1, iterations + 1):
        best_move = None
        best_move_score = float("-inf")

        for person_a, person_b in _sample_pairs(rng, seat_indices, neighborhood_size):
            move = _move_key(person_a, person_b)
            is_tabu = tabu_until.get(move, 0) > iteration

            candidate_score = _score_after_swap(arrangement, current_score, person_a, person_b)
            if is_tabu and candidate_score <= best_score:
                continue

            if candidate_score > best_move_score:
                best_move = (person_a, person_b, move)
                best_move_score = candidate_score

        if best_move is None:
            break

        person_a, person_b, move = best_move
        switch(arrangement, person_a, person_b)
        current_score = best_move_score
        tabu_until[move] = iteration + tabu_tenure

        if current_score > best_score:
            best_score = current_score
            best_arrangement = deepcopy(arrangement)
            no_improve = 0
        else:
            no_improve += 1

        if no_improve >= max_no_improve:
            break

        if iteration % 50 == 0:
            tabu_until = {k: v for k, v in tabu_until.items() if v > iteration}

    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    return arrangement

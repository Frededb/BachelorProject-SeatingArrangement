import random
import time
from copy import deepcopy

from Utils.UtilFunctions import switch, getAllPeople
from Utils.ValueCalc import calcArrangement, calcTable


def _score_after_swap(arrangement, current_score, person_a, person_b):
    """Return the arrangement score after a temporary swap of two people."""
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


def randomSwitch(arrangement, N=None, seed=None, max_seconds=None, score_tracker=None):
    rng = random.Random(seed)
    seat_indices = getAllPeople(arrangement)
    people_count = len(seat_indices)
    if N is None:
        if people_count <= 30:
            N = 300 * people_count
        elif people_count <= 120:
            N = 200 * people_count
        else:
            N = 120 * people_count
        N = max(2000, N)

    start_time = time.perf_counter()
    current_score = calcArrangement(arrangement)[0]
    best_score = current_score
    best_arrangement = deepcopy(arrangement)
    for i in range(N):
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break

        personA, personB = rng.sample(seat_indices, 2)
        new_score = _score_after_swap(arrangement, current_score, personA, personB)
        if new_score < current_score:
            continue
        else:
            switch(arrangement, personA, personB)
            current_score = new_score

        if current_score > best_score:
            best_score = current_score
            best_arrangement = deepcopy(arrangement)
            if score_tracker is not None:
                score_tracker[0] = best_score

    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    return arrangement






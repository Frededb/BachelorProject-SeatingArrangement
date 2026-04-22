import random
import time
from copy import deepcopy
from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import switch, getAllPeople

def randomSwitch(arrangement, N=None, seed=None, max_seconds=None):
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
    current_score, _, _ = calcArrangement(arrangement)
    best_score = current_score
    best_arrangement = deepcopy(arrangement)
    for i in range(N):
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break

        personA, personB = rng.sample(seat_indices, 2)
        switch(arrangement, personA, personB)
        new_score, _, _ = calcArrangement(arrangement)
        if new_score < current_score:
            switch(arrangement, personA, personB)
        else:
            current_score = new_score

        if current_score > best_score:
            best_score = current_score
            best_arrangement = deepcopy(arrangement)

    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    return arrangement

    

    


from Utils.ValueCalc import calcTable, calcArrangement
from itertools import permutations
import math
import time

arrangement = []

def get_2d_permutations(arrangement):
    # 1. Flatten into a single list
    flat_list = [person for table in arrangement for person in table]

    # 2. Generate all permutations
    for perm in permutations(flat_list):
        
        # 3. Split back into arrangements
        perm_iter = iter(perm)
        new_arrangement = [
            [next(perm_iter) for _ in table] for table in arrangement
        ]
        yield new_arrangement

def bruteForce(initialArrangement, max_seconds=None, score_tracker=None):
    #here I will generate all permutations of input
    all_arrangements = get_2d_permutations(initialArrangement)
    bestValue = -math.inf
    bestArrangement = []

    start_time = time.time()

    #we go through each and see if they are better than the previous best
    for arrangement in all_arrangements:
        if max_seconds is not None and time.time() - start_time > max_seconds:
            break

        permValue = calcArrangement(arrangement)[0]

        if permValue > bestValue:
            bestValue = permValue
            bestArrangement = arrangement
            if score_tracker is not None:
                score_tracker[0] = bestValue
    return bestArrangement

def bruteForceEachTable(initialArrangement):
    bestValue = -math.inf
    bestArrangement = []

    # we go through each and see if they are better than the previous best
    for table in initialArrangement:
        tablePerms = permutations(table)
        bestValue = -math.inf
        bestTable = []
        for perm in tablePerms:
            tableValue = calcTable(list(perm))[0]

            if tableValue > bestValue:
                bestValue = tableValue
                bestTable = list(perm)
        bestArrangement.append(bestTable)
    return bestArrangement

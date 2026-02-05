from Utils.ValueCalc import calcTable, calcArrangement
from itertools import islice, permutations
import math

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

def bruteForce(initialArrangement):
    #here I will generate all permutations of input
    all_arrangements = permutations(initialArrangement)
    bestValue = -math.inf
    bestArrangement = -1

    #we go through each and see if they are better than the previous best
    for arrangement in all_arrangements:
        permValue = calcArrangement(arrangement)[0]

        if permValue > bestValue:
            bestValue = permValue
            bestArrangement = arrangement
    return bestArrangement


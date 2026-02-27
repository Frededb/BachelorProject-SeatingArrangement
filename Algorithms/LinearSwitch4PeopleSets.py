import itertools
from time import perf_counter

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import getAllPeople, switch4People, switch4PeopleBack


def LinearSwitch4PeopleSets(arrangement):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 4 people
    combinations = itertools.combinations(allPeople, 4)
    count = 0
    for combination in combinations:
        permutations = itertools.permutations(combination)
        for permutation in permutations:

            # python
            # Replace the per-person table reads with a unique set of affected table indices
            affected_tables = {p[0] for p in permutation}  # unique table indices affected by this 4-person swap

            preValueTotal = sum(calcTable(arrangement[idx])[0] for idx in affected_tables)

            switch4People(arrangement, permutation[0], permutation[1], permutation[2], permutation[3])

            postValueTotal = sum(calcTable(arrangement[idx])[0] for idx in affected_tables)

            if postValueTotal < preValueTotal:
                switch4PeopleBack(arrangement, permutation[0], permutation[1], permutation[2], permutation[3])

        count += 1
        if count % 100000 == 0:
            count = 0
            print(f"Finished checking combinations for set: {combination}")

    return arrangement
import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.UtilFunctions import getAllPeople, switch4People, switch4PeopleBack


def LinearSwitch4PeopleSets(arrangement, coords=None):
    if coords is None:
        coords = getAllPeople(arrangement)

    #generate all permutations of 4 people
    permutations = itertools.permutations(coords, 4)
    count = 0
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


        if count % 10000000 == 0:
            print(f"Checked {count/110355024*100} %")

    return arrangement

def linearSwitch4PeopleEachTable(initialArrangement):
    bestArrangement = []

    # Optimize each table independently using linear 4-person switches.
    for table in initialArrangement:
        optimizedSingleTable = LinearSwitch4PeopleSets([list(table)])
        bestArrangement.append(optimizedSingleTable[0])
    return bestArrangement

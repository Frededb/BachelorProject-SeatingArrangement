import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import getAllPeople, switch4People, switch4PeopleBack


def LinearSwitch4PeopleSets(arrangement):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 4 people
    combinations = itertools.combinations(allPeople, 4)
    count = 0
    for combination in combinations:
        #generate all permutations of the 4 people
        permutations = itertools.permutations(combination)
        for permutation in permutations:

            preValueTotal = calcArrangement(arrangement)

            switch4People(arrangement, permutation[0], permutation[1], permutation[2], permutation[3])

            postValueTotal = calcArrangement(arrangement)

            if postValueTotal < preValueTotal:
                switch4PeopleBack(arrangement, permutation[0], permutation[1], permutation[2], permutation[3])  # Switch back if no improvementt))
        count += 1
        if count % 100000 == 0:
            count = 0
            print(f"Finished checking combinations for set: {combination}")
    return arrangement
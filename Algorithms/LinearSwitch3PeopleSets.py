import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import getAllPeople, switch4People, switch4PeopleBack, switch3People, switch3PeopleBack


def LinearSwitch3PeopleSets(arrangement):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 3 people
    combinations = itertools.combinations(allPeople, 3)
    count = 0
    for combination in combinations:
        #generate all permutations of the 3 people
        permutations = itertools.permutations(combination)
        for permutation in permutations:

            preValueTotal = calcArrangement(arrangement)

            switch3People(arrangement, permutation[0], permutation[1], permutation[2])

            postValueTotal = calcArrangement(arrangement)

            if postValueTotal < preValueTotal:
                switch3PeopleBack(arrangement, permutation[0], permutation[1], permutation[2])  # Switch back if no improvementt))
        count += 1
        if count % 100000 == 0:
            count = 0
            print(f"Finished checking combinations for set: {combination}")
    return arrangement
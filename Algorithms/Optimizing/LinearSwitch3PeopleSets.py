import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.UtilFunctions import getAllPeople, switch4People, switch4PeopleBack, switch3People, switch3PeopleBack


def LinearSwitch3PeopleSets(arrangement):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 3 people
    permutations = itertools.permutations(allPeople, 3)
    for permutation in permutations:
        preValueTotal = calcArrangement(arrangement)[0]

        switch3People(arrangement, permutation[0], permutation[1], permutation[2])

        postValueTotal = calcArrangement(arrangement)[0]

        if postValueTotal < preValueTotal:
            switch3PeopleBack(arrangement, permutation[0], permutation[1], permutation[2])  # Switch back if no improvementt))
    return arrangement
import itertools

from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import getAllPeople, switch


def LinearSwitch2PeopleSets(arrangement):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 2 people
    combinations = itertools.combinations(allPeople, 2)
    for personA, personB in combinations:
        preValueTotal = calcArrangement(arrangement)[0]

        switch(arrangement, personA, personB)

        postValueTotal = calcArrangement(arrangement)[0]

        if postValueTotal < preValueTotal:
            switch(arrangement, personA, personB)  # Switch back if no improvementt))
    return arrangement
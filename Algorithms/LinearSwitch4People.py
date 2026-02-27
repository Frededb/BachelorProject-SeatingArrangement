import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople, switch3People, switch3PeopleBack, switch4People, switch4PeopleBack


def LinearSwitch4People(arrangement):
    allPeople = getAllPeople(arrangement)
    for personA in allPeople:
        for personB in allPeople:
            for personC in allPeople:
                for personD in allPeople:

                    preValueTotal = calcArrangement(arrangement)

                    switch4People(arrangement, personA, personB, personC, personD)

                    postValueTotal = calcArrangement(arrangement)

                    if postValueTotal < preValueTotal:
                        switch4PeopleBack(arrangement, personA, personB, personC, personD)  # Switch back if no improvementt))
        print(f"Finished checking combinations for personA: {personA}")
    return arrangement
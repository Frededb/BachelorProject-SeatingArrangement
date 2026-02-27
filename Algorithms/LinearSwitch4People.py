import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople, switch3People, switch3PeopleBack, switch4People, switch4PeopleBack


def LinearSwitch4People(arrangement):
    allPeople = getAllPeople(arrangement)
    for personA in allPeople:
        for personB in allPeople:
            if personA == personB:
                continue
            for personC in allPeople:
                if personC == personA or personC == personB:
                    continue
                for personD in allPeople:
                    if personD == personA or personD == personB or personD == personC:
                        continue
                    preValueTotal = calcArrangement(arrangement)[0]

                    switch4People(arrangement, personA, personB, personC, personD)

                    postValueTotal = calcArrangement(arrangement)[0]

                    if postValueTotal < preValueTotal:
                        switch4PeopleBack(arrangement, personA, personB, personC, personD)  # Switch back if no improvementt))
        print(f"Finished checking combinations for personA: {personA}")
    return arrangement
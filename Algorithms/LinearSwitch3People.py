import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople, switch3People, switch3PeopleBack
from Utils.printer import printArrangementWithValues


def LinearSwitch3People(arrangement):
    allPeople = getAllPeople(arrangement)
    for personA in allPeople:
        for personB in allPeople:
            for personC in allPeople:
                if personA == personB or personA == personC or personB == personC:
                    continue

                preValueTotal = calcArrangement(arrangement)[0]

                switch3People(arrangement, personA, personB, personC)

                postValueTotal = calcArrangement(arrangement)[0]

                if postValueTotal < preValueTotal:
                    switch3PeopleBack(arrangement, personA, personB, personC)  # Switch back if no improvementt))
    return arrangement
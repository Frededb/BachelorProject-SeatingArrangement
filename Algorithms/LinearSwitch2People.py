from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople


def LinearSwitch2People(arrangement):
    allPeople = getAllPeople(arrangement)
    for personA in allPeople:
        for personB in allPeople:
            if personA == personB:
                continue

            preValueTableA = calcTable(arrangement[personA[0]])[0]
            preValueTableB = calcTable(arrangement[personB[0]])[0]
            preValueTotal = preValueTableA + preValueTableB

            switch(arrangement, personA, personB)
            postValueTableA = calcTable(arrangement[personA[0]])[0]
            postValueTableB = calcTable(arrangement[personB[0]])[0]
            postValueTotal = postValueTableA + postValueTableB

            if postValueTotal < preValueTotal:
                switch(arrangement, personA, personB)  # Switch back if no improvement
    return arrangement
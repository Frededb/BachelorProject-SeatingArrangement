from Utils.ValueCalc import calcTable
from Utils.bmalls import switch, getAllPeople


def LinearSwitch(arrangement):
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
            else:
                print(f"Switched {arrangement[personB[0]][personB[1]].name} and {arrangement[personA[0]][personA[1]].name} for improvement from {preValueTotal} to {postValueTotal}")

    return arrangement
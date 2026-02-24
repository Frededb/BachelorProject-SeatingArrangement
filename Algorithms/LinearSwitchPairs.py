from Algorithms.findPairs import findPairs
from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople, switchPair


def LinearSwitchPairs(arrangement, pairs, N):
    for count in range(N):
        for pair in pairs:
            personA = pair[0]
            personB = pair[1]

            #find the coordinates of personA and personB
            personACoords = None
            personBCoords = None
            for i in range(len(arrangement)):
                for j in range(len(arrangement[i])):
                    if arrangement[i][j].name == personA.name:
                        personACoords = (i, j)
                    if arrangement[i][j].name == personB.name:
                        personBCoords = (i, j)

            pairCoords = (personACoords, personBCoords)

            for table in arrangement:
                for i in range(len(table)-1):

                    preValueTableA = calcTable(arrangement[personACoords[0]])[0]
                    preValueTableB = calcTable(arrangement[personBCoords[0]])[0]
                    preValueTableC = calcTable(table)[0]
                    preValueTotal = preValueTableA + preValueTableB + preValueTableC

                    switchPair(arrangement, pairCoords, (table[i], table[i+1]))

                    postValueTableA = calcTable(arrangement[personACoords[0]])[0]
                    postValueTableB = calcTable(arrangement[personBCoords[0]])[0]
                    postValueTableC = calcTable(table)[0]
                    postValueTotal = postValueTableA + postValueTableB + postValueTableC

                    if postValueTotal < preValueTotal:
                        switchPair(arrangement, pairCoords, (table[i], table[i+1]))  # Switch back if no improvement

            for table in arrangement:
                for i in range(len(table)//2):

                    preValueTableA = calcTable(arrangement[personACoords[0]])[0]
                    preValueTableB = calcTable(arrangement[personBCoords[0]])[0]
                    preValueTableC = calcTable(table)[0]
                    preValueTotal = preValueTableA + preValueTableB + preValueTableC

                    switchPair(arrangement, pairCoords, (table[i], table[i + 4]))

                    postValueTableA = calcTable(arrangement[personACoords[0]])[0]
                    postValueTableB = calcTable(arrangement[personBCoords[0]])[0]
                    postValueTableC = calcTable(table)[0]
                    postValueTotal = postValueTableA + postValueTableB + postValueTableC

                    if postValueTotal < preValueTotal:
                        switchPair(arrangement, pairCoords, (table[i], table[i + 1]))  # Switch back if no improvement

        print(f"Iteration {count} complete with value: {calcArrangement(arrangement)}")
    return arrangement
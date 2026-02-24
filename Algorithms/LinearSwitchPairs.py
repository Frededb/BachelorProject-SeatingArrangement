from Algorithms.findPairs import findPairs
from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople, switchPair
from Utils.printer import printTableWithValues


def LinearSwitchPairs(arrangement, pairs, N):
    for count in range(N):
        print(pairs)
        for pair in pairs:
            personA = list(pair)[0]
            personB = list(pair)[1]

            for i in range(len(arrangement)):
                table = arrangement[i]

                # find the coordinates of personA and personB
                personACoords = None
                personBCoords = None
                for i in range(len(arrangement)):
                    for j in range(len(arrangement[i])):
                        if arrangement[i][j].name == personA.name:
                            personACoords = (i, j)
                        if arrangement[i][j].name == personB.name:
                            personBCoords = (i, j)

                pairCoords = (personACoords, personBCoords)


                for j in range(len(table)-1):
                    preValueTableA = calcTable(arrangement[personACoords[0]])[0]
                    preValueTableB = calcTable(arrangement[personBCoords[0]])[0]
                    preValueTableC = calcTable(table)[0]
                    preValueTotal = preValueTableA + preValueTableB + preValueTableC

                    tmpTable = table.copy()

                    switchPair(arrangement, pairCoords, ((i, j), (i, j+1)))

                    postValueTableA = calcTable(arrangement[personACoords[0]])[0]
                    postValueTableB = calcTable(arrangement[personBCoords[0]])[0]
                    postValueTableC = calcTable(table)[0]
                    postValueTotal = postValueTableA + postValueTableB + postValueTableC

                    if postValueTotal < preValueTotal:
                        switchPair(arrangement, pairCoords, ((i, j), (i, j+1)))  # Switch back if no improvement
                    else:
                        print("===========================")
                        printTableWithValues(tmpTable)
                        print(f"Switched pair {personA.name} and {personB.name} with table {i} for improvement from {preValueTotal/3} to {postValueTotal/3}")
                        printTableWithValues(table)


            # for i in range(len(arrangement)):
            #     table = arrangement[i]
            #     for j in range(len(table)//2):
            #
            #         preValueTableA = calcTable(arrangement[personACoords[0]])[0]
            #         preValueTableB = calcTable(arrangement[personBCoords[0]])[0]
            #         preValueTableC = calcTable(table)[0]
            #         preValueTotal = preValueTableA + preValueTableB + preValueTableC
            #
            #         switchPair(arrangement, pairCoords, ((i, j), (i, j+4)))
            #
            #         postValueTableA = calcTable(arrangement[personACoords[0]])[0]
            #         postValueTableB = calcTable(arrangement[personBCoords[0]])[0]
            #         postValueTableC = calcTable(table)[0]
            #         postValueTotal = postValueTableA + postValueTableB + postValueTableC
            #
            #         if postValueTotal < preValueTotal:
            #             switchPair(arrangement, pairCoords, ((i, j), (i, j+4)))  # Switch back if no improvement

        print(f"Iteration {count} complete with value: {calcArrangement(arrangement)}")
    return arrangement
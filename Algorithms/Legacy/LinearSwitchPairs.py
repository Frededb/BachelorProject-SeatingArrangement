from Utils.ValueCalc import calcArrangement
from Utils.bmalls import switchPair, switchPairBack


def LinearSwitchPairs(arrangement, pairs):
    for pair in pairs:
        personA = list(pair)[0]
        personB = list(pair)[1]

        # find the coordinates of personA and personB
        personACoords = None
        personBCoords = None
        for i in range(len(arrangement)):
            if personACoords is not None and personBCoords is not None:
                break
            for j in range(len(arrangement[i])):
                if arrangement[i][j].name == personA.name:
                    personACoords = (i, j)
                if arrangement[i][j].name == personB.name:
                    personBCoords = (i, j)

        pairCoords = (personACoords, personBCoords)

        for i in range(len(arrangement)):
            table = arrangement[i]
            for j in range(len(table)-1):
                preValueTotal = calcArrangement(arrangement)[0]

                switchPair(arrangement, pairCoords, ((i, j), (i, j+1)))

                postValueTotal = calcArrangement(arrangement)[0]

                if postValueTotal < preValueTotal:
                    switchPairBack(arrangement, pairCoords, ((i, j), (i, j+1)))  # Switch back if no improvement
                else:
                    # Give them the new coords
                    pairCoords = ((i, j), (i, j+1))

        for i in range(len(arrangement)):
            table = arrangement[i]
            for j in range(len(table)//2):
                preValueTotal = calcArrangement(arrangement)[0]

                switchPairBack(arrangement, pairCoords, ((i, j), (i, j+4)))

                postValueTotal = calcArrangement(arrangement)[0]

                if postValueTotal < preValueTotal:
                    switchPair(arrangement, pairCoords, ((i, j), (i, j+4)))  # Switch back if no improvement
                else:
                    # Give them the new coords
                    pairCoords = ((i, j), (i, j+4))
    return arrangement
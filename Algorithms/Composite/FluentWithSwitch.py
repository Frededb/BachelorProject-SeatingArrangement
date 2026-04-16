from Algorithms.GroupBuild.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.LinearSwitchPeopleSets import linearSwitchPeopleEachTable, LinearSwitchPeopleSets
from Utils.ValueCalc import calcArrangement


def FluentWithSwitch(input, emptyArrangement):

    emptyArrangement, protectedNames = fluentGroupsFill(input, emptyArrangement, False)

    emptyArrangement = linearSwitchPeopleEachTable(emptyArrangement, 4)
    # emptyArrangement = bruteForceEachTable(emptyArrangement)
    # print("score after first: ", calcArrangement(emptyArrangement)[0])

    movableCoords = [
        (tableIndex, seatIndex)
        for tableIndex, table in enumerate(emptyArrangement)
        for seatIndex, person in enumerate(table)
        if person.name not in protectedNames
    ]

    emptyArrangement = LinearSwitchPeopleSets(emptyArrangement, 4, movableCoords)
    # print("score after linear switch4people: ", calcArrangement(emptyArrangement)[0])


    return emptyArrangement
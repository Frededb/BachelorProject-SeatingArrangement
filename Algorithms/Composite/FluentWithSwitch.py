from Algorithms.GroupBuild.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.BruteForce import bruteForceEachTable
from Algorithms.Optimizing.LinearSwitch4PeopleSets import linearSwitch4PeopleEachTable, LinearSwitch4PeopleSets
from Utils.ValueCalc import calcArrangement


def FluentWithSwitch(input, emptyArrangement):

    emptyArrangement, protectedNames = fluentGroupsFill(input, emptyArrangement, True)

    # emptyArrangement = linearSwitch4PeopleEachTable(emptyArrangement)
    emptyArrangement = bruteForceEachTable(emptyArrangement)
    print("score after first: ", calcArrangement(emptyArrangement)[0])

    movableCoords = [
        (tableIndex, seatIndex)
        for tableIndex, table in enumerate(emptyArrangement)
        for seatIndex, person in enumerate(table)
        if person.name not in protectedNames
    ]

    emptyArrangement = LinearSwitch4PeopleSets(emptyArrangement)
    print("score after linear switch4people: ", calcArrangement(emptyArrangement)[0])


    return emptyArrangement
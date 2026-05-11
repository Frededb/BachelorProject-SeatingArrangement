from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.LinearSwitchPeopleSets import linearSwitchPeopleEachTable
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch
from Utils.ValueCalc import calcArrangement


def linearSwitchFromGroupedProtected(input, emptyArrangement, max_seconds=None, score_tracker=None):

    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)

    arrangement = linearSwitchPeopleEachTable(arrangement, 4)

    if score_tracker is not None:
        score_tracker[0] = calcArrangement(arrangement)[0]

    movableCoords = [
        (tableIndex, seatIndex)
        for tableIndex, table in enumerate(arrangement)
        for seatIndex, person in enumerate(table)
        if person.name not in protectedNames
    ]

    arrangement = repeatedLinearSwitch(arrangement, 4, movableCoords, max_seconds=max_seconds, score_tracker=score_tracker)

    return arrangement
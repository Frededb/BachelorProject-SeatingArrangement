from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.LinearSwitchPeopleSets import linearSwitchPeopleEachTable
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromFluentProtected(input, emptyArrangement, max_seconds=None):

    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)

    arrangement = linearSwitchPeopleEachTable(arrangement, 4)

    movableCoords = [
        (tableIndex, seatIndex)
        for tableIndex, table in enumerate(arrangement)
        for seatIndex, person in enumerate(table)
        if person.name not in protectedNames
    ]

    arrangement = repeatedLinearSwitch(arrangement, 4, movableCoords, max_seconds=max_seconds)

    return arrangement
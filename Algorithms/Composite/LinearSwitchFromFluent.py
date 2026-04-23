from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromFluent(input, emptyArrangement, max_seconds=None):

    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)

    arrangement = repeatedLinearSwitch(arrangement, 3, max_seconds=max_seconds)

    return arrangement
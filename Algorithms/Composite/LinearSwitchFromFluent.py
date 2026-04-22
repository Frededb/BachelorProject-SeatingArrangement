from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromFluent(input, emptyArrangement):

    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)

    arrangement = repeatedLinearSwitch(arrangement, 3)

    return arrangement
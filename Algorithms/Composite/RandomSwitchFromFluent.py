from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromFluent(input, emptyArrangement):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = randomSwitch(arrangement)
    return arrangement


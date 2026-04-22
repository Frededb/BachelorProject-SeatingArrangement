from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromFluent(input, emptyArrangement, max_seconds=None):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = randomSwitch(arrangement, max_seconds=max_seconds)
    return arrangement


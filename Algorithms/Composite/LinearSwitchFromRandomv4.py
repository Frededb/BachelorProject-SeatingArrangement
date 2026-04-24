from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromRandomv4(input, emptyArrangement, max_seconds=None):

    arrangement = randomPlacement(input, emptyArrangement)

    arrangement = repeatedLinearSwitch(arrangement, 4, max_seconds=max_seconds)

    return arrangement
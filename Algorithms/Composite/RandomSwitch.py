from Algorithms.Build.RandomPlacement import RandomPlacement
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromRandom(input, emptyArrangement):
    arrangement = RandomPlacement(input, emptyArrangement)
    return randomSwitch(arrangement)


from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    return randomSwitch(arrangement)


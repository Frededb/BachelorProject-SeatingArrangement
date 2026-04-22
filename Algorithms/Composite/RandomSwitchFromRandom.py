from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromRandom(input, emptyArrangement, max_seconds=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = randomSwitch(arrangement, max_seconds=max_seconds)
    return arrangement


from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromRandom(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = randomSwitch(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement


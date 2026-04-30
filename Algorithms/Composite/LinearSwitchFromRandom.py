from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromRandom(input, emptyArrangement, max_seconds=None, score_tracker=None):

    arrangement = randomPlacement(input, emptyArrangement)

    arrangement = repeatedLinearSwitch(arrangement, 3, max_seconds=max_seconds, score_tracker=score_tracker)

    return arrangement
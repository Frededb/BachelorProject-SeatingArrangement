from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.RandomSwitch import randomSwitch


def randomSwitchFromGrouped(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = randomSwitch(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement


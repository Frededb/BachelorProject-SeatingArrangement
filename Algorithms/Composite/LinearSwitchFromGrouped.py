from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromGrouped(input, emptyArrangement, max_seconds=None, score_tracker=None):

    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)

    arrangement = repeatedLinearSwitch(arrangement, 3, max_seconds=max_seconds, score_tracker=score_tracker)

    return arrangement
from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.TabuSearch import tabuSearch


def tabuSearchFromFluent(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = tabuSearch(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement


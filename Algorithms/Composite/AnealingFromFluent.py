from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.Anealing import annealing


def annealingFromFluent(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = annealing(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement
from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.Anealing import annealing

def annealingFromGrouped(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement, _ = fluentGroupsFill(input, emptyArrangement)

    return annealing(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)

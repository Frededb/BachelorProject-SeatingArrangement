from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.Anealing import annealing


def annealingFromRandom(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = annealing(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement


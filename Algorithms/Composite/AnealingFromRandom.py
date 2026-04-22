from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.Anealing import annealing


def annealingFromRandom(input, emptyArrangement, max_seconds=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = annealing(arrangement, max_seconds=max_seconds)
    return arrangement


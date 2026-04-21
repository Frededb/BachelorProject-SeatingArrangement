from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.Anealing import annealing


def annealingFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = annealing(arrangement)
    return arrangement


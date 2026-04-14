from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.BruteForce import bruteForce


def bruteForceFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    return bruteForce(arrangement)


from Algorithms.Build.RandomPlacement import RandomPlacement
from Algorithms.Optimizing.BruteForce import bruteForce


def bruteForceFromRandom(input, emptyArrangement):
    arrangement = RandomPlacement(input, emptyArrangement)
    return bruteForce(arrangement)


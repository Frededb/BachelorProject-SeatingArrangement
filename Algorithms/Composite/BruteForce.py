from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.BruteForce import bruteForce


def bruteForceFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = bruteForce(arrangement)
    return arrangement


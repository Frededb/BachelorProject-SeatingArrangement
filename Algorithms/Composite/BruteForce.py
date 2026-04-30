from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.BruteForce import bruteForce


def bruteForceFromRandom(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = bruteForce(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement


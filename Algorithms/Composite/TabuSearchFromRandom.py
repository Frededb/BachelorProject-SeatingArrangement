from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.TabuSearch import tabuSearch


def tabuSearchFromRandom(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = tabuSearch(arrangement, max_seconds=max_seconds, score_tracker=score_tracker)
    return arrangement
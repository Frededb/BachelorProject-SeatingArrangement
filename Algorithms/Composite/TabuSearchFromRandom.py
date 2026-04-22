from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.TabuSearch import tabuSearch


def tabuSearchFromRandom(input, emptyArrangement, max_seconds=None):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = tabuSearch(arrangement, max_seconds=max_seconds)
    return arrangement
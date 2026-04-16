from Algorithms.Build.RandomPlacement import RandomPlacement
from Algorithms.Optimizing.tabuSearch import tabuSearch


def tabuSearchFromRandom(input, emptyArrangement):
    arrangement = RandomPlacement(input, emptyArrangement)
    return tabuSearch(arrangement)


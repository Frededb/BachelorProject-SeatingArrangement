from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.TabuSearch import tabuSearch


def tabuSearchFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    arrangement = tabuSearch(arrangement)
    return arrangement
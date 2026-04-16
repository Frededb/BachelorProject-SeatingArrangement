from Algorithms.Build.RandomPlacement import RandomPlacement
from Algorithms.Optimizing.Anealing import AnealTwoPeople


def anealingFromRandom(input, emptyArrangement):
    arrangement = RandomPlacement(input, emptyArrangement)
    return AnealTwoPeople(arrangement)


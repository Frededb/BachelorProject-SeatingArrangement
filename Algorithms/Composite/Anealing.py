from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.Anealing import AnealTwoPeople


def anealingFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    return AnealTwoPeople(arrangement)


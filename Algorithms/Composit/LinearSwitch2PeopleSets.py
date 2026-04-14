from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.LinearSwitch2PeopleSets import LinearSwitch2PeopleSets


def linearSwitch2PeopleSetsFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    return LinearSwitch2PeopleSets(arrangement)


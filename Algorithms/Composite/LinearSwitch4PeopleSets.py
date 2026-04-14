from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets


def linearSwitch4PeopleSetsFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    return LinearSwitch4PeopleSets(arrangement)


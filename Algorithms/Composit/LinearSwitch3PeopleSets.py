from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.LinearSwitch3PeopleSets import LinearSwitch3PeopleSets


def linearSwitch3PeopleSetsFromRandom(input, emptyArrangement):
    arrangement = randomPlacement(input, emptyArrangement)
    return LinearSwitch3PeopleSets(arrangement)


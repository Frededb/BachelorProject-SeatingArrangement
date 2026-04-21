from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch


def linearSwitchFromRandom(input, emptyArrangement):

    arrangement = randomPlacement(input, emptyArrangement)

    arrangement = repeatedLinearSwitch(arrangement, 3)

    return arrangement
from Algorithms.GroupBuild.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.TabuSearch import tabuSearch


def tabuSearchFromFluent(input, emptyArrangement):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = tabuSearch(arrangement)
    return arrangement


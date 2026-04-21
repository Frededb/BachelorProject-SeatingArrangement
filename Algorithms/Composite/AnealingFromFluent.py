from Algorithms.GroupBuild.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.Anealing import annealing


def annealingFromFluent(input, emptyArrangement):
    arrangement, protectedNames = fluentGroupsFill(input, emptyArrangement)
    arrangement = annealing(arrangement)
    return arrangement
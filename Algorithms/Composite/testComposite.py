from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Composite.FluentWithSwitch import FluentWithSwitch
from Algorithms.Optimizing.LinearSwitch2PeopleSets import LinearSwitch2PeopleSets
from Algorithms.Optimizing.tabuSearch import tabuSearch


def testComposite(input, emptyArrangement):
    from Algorithms.Optimizing.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets

    arrangement = FluentWithSwitch(input, emptyArrangement)

    arrangement = LinearSwitch4PeopleSets(arrangement)

    arrangement = LinearSwitch4PeopleSets(arrangement)
    arrangement = LinearSwitch4PeopleSets(arrangement)

    arrangement = tabuSearch(arrangement)

    arrangement = LinearSwitch4PeopleSets(arrangement)

    arrangement = LinearSwitch4PeopleSets(arrangement)
    arrangement = LinearSwitch4PeopleSets(arrangement)

    arrangement = LinearSwitch2PeopleSets(arrangement)

    arrangement = LinearSwitch2PeopleSets(arrangement)
    arrangement = LinearSwitch2PeopleSets(arrangement)

    arrangement = LinearSwitch4PeopleSets(arrangement)
    arrangement = LinearSwitch4PeopleSets(arrangement)

    arrangement = LinearSwitch2PeopleSets(arrangement)

    return arrangement
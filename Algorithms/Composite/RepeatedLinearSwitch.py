from Algorithms.Build.RandomPlacement import RandomPlacement
from Algorithms.Optimizing.LinearSwitchPeopleSets import LinearSwitchPeopleSets
from Utils.ValueCalc import calcArrangement


def RepeatedLinearSwitch(input, emptyArrangement):
    arrangement = RandomPlacement(input, emptyArrangement)
    best_arrangement = arrangement
    best_score = calcArrangement(arrangement)[0]
    previous_score = best_score

    while True:
        arrangement = LinearSwitchPeopleSets(arrangement, 4)
        score = calcArrangement(arrangement)[0]

        if score > best_score:
            best_score = score
            best_arrangement = arrangement

        if score == previous_score:
            return best_arrangement

        previous_score = score

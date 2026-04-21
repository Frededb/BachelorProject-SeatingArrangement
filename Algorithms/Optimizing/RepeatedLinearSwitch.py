from Algorithms.Optimizing.LinearSwitchPeopleSets import LinearSwitchPeopleSets
from Utils.ValueCalc import calcArrangement


def repeatedLinearSwitch(arrangement, v, movableCoords = None):
    best_arrangement = arrangement
    best_score = calcArrangement(arrangement)[0]
    previous_score = best_score

    while True:
        arrangement = LinearSwitchPeopleSets(arrangement, v, movableCoords)
        score = calcArrangement(arrangement)[0]

        if score > best_score:
            best_score = score
            best_arrangement = arrangement

        if score == previous_score:
            return best_arrangement

        previous_score = score

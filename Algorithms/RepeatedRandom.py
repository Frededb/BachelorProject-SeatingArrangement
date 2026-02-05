from Algorithms.Random import randomArrangement
import math

from Utils.ValueCalc import calcArrangement


def repeatedRandom(counter, input):
    bestArrangement = []
    bestValue = -math.inf
    for _ in range(counter):
        arrangement = randomArrangement(input)
        value = calcArrangement(arrangement)[0]
        if value > bestValue:
            bestArrangement = arrangement
            bestValue = value
    return bestArrangement
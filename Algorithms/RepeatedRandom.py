from Algorithms.Random import randomArrangement
import math

from Utils.ValueCalc import calcArrangement


def repeatedRandom(input, N):
    bestArrangement = []
    bestValue = -math.inf
    for _ in range(N):
        arrangement = randomArrangement(input)
        value = calcArrangement(arrangement)[0]
        if value > bestValue:
            bestArrangement = arrangement
            bestValue = value
    return bestArrangement
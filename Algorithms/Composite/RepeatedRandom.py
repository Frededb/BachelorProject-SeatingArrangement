from Algorithms.Build.RandomPlacement import RandomPlacement
import math

from Utils.ValueCalc import calcArrangement

def repeatedRandom(input, emptyArrangement):
    bestArrangement = []
    bestValue = -math.inf
    for _ in range(100):
        arrangement = RandomPlacement(input, emptyArrangement)
        value = calcArrangement(arrangement)[0]
        if value > bestValue:
            bestArrangement = arrangement
            bestValue = value
    return bestArrangement
from Utils.ValueCalc import calcTable, calcArrangement
from itertools import permutations
import math

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    arrangement = [[0,0,0,0,0,0,0,0]]*math.ceil(arrangementSize/8)

def bruteForce(input):
    newArrangement(len(input)/8)
    all_perms = list(permutations(input))
    bestValue = -math.inf
    bestArrangement = -1
    for perm in all_perms:
        permValue = makeArrangement(perm)
        if(permValue) > bestValue:
            bestValue = permValue
            bestArrangement = arrangement
    return bestArrangement

def makeArrangement(perm):
    global arrangement
    for i in range(perm):
        arrangement[i//8][i%8] = perm[i]
    return calcArrangement(arrangement)
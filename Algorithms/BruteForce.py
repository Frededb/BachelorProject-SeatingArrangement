from Utils.ValueCalc import calcTable, calcArrangement
from itertools import islice, permutations
import math

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    arrangement = [[0] * 8 for _ in range(math.ceil(arrangementSize/8))]

def makeArrangement(perm):
    global arrangement
    for i in range(len(perm)):
        arrangement[i//8][i%8] = perm[i]
    return calcArrangement(arrangement)[0]

def bruteForce(input):
    newArrangement(len(input))
    #here I will generate all permutations of input
    all_perms = permutations(input)
    bestValue = -math.inf
    bestArrangement = -1

    #we go through each and see if they are better than the previous best
    for perm in all_perms:
        permValue = makeArrangement(perm)

        if permValue > bestValue:
            bestValue = permValue
            bestArrangement = [row[:] for row in arrangement]
    return bestArrangement


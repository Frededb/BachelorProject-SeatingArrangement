from Utils.ValueCalc import calcTable
import math
import random

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    arrangement = [[0] * 8 for _ in range(math.ceil(arrangementSize/8))]

def randomGreedy(input):
    newArrangement(len(input))
    for _ in range(len(input)):
        number = random.randint(0,len(input)-1)
        person = input.pop(number)
        placeGreedy(person)
    return arrangement


def placeGreedy(person):
    global arrangement
    bestImprovement = -math.inf
    bestPlacement = (-1,-1)
    for i in range(len(arrangement)):
        preValue = calcTable(arrangement[i])
        for j in range(len(arrangement[i])):
            if arrangement[i][j] != 0:
                continue
            arrangement[i][j] = person
            postValue = calcTable(arrangement[i])
            # print(f"preValue:  {preValue} postValue:  {postValue} improvement:  {(postValue - preValue)} bestImprovement: {bestImprovement}")
            if postValue - preValue > bestImprovement:
                bestImprovement = postValue - preValue
                bestPlacement = (i,j)
            arrangement[i][j] = 0
    arrangement[bestPlacement[0]][bestPlacement[1]] = person




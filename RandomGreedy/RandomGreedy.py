from Utils.ValueCalc import calcTable
import math

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    arrangement = [[0,0,0,0,0,0,0,0]]*math.ceil(arrangementSize/8)

def randomGreedy(input):
    newArrangement(len(input)/8)
    import random
    for _ in range(len(input)):
        number = random.random(len(input))
        placeGreedy(input[number])
    return arrangement


def placeGreedy(person):
    global arrangement
    bestImprovement = -1000
    bestPlacement = (-1,-1)
    for i in range(len(arrangement)):
        for j in range(len(arrangement[i])):
            if(arrangement[i][j] != 0):
                continue
            preValue = calcTable(arrangement[i])
            arrangement[i][j] = person
            postValue = calcTable(arrangement[i])
            if postValue - preValue > bestImprovement:
                bestImprovement = postValue - preValue
                bestPlacement = (i,j)
            arrangement[i][j] = 0
    arrangement[bestPlacement[0]][bestPlacement[1]] = person




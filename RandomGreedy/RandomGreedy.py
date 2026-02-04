from Utils.ValueCalc import calcTable
import math
import random

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    #sets up the arrangement 2d array based on input size
    arrangement = [[None] * 8 for _ in range(math.ceil(arrangementSize/8))]

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
        preValue = calcTable(arrangement[i])[0]
        for j in range(len(arrangement[i])):
            #if the spot is already taken, skip
            if arrangement[i][j] != None:
                continue
            arrangement[i][j] = person
            postValue = calcTable(arrangement[i])[0]
            #here we find the best improvement to a single table, which should give the best improvement overall
            if postValue - preValue > bestImprovement:
                bestImprovement = postValue - preValue
                bestPlacement = (i,j)
            arrangement[i][j] = 0
    arrangement[bestPlacement[0]][bestPlacement[1]] = person




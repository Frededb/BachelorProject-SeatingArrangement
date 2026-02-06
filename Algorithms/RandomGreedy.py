from copy import deepcopy

from Utils.ValueCalc import calcTable
import math
import random

from Utils.reader import emptyPerson

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    #sets up the arrangement 2d array based on input size
    arrangement = [[emptyPerson] * 8 for _ in range(math.ceil(arrangementSize/8))]

def randomGreedy(input):
    inputCopy = deepcopy(input)
    newArrangement(len(inputCopy))
    for _ in range(len(inputCopy)):
        number = random.randint(0,len(inputCopy)-1)
        person = inputCopy.pop(number)
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
            if arrangement[i][j].name != "Empty":
                continue
            arrangement[i][j] = person
            postValue = calcTable(arrangement[i])[0]
            #here we find the best improvement to a single table, which should give the best improvement overall
            if postValue - preValue > bestImprovement:
                bestImprovement = postValue - preValue
                bestPlacement = (i,j)
            arrangement[i][j] = emptyPerson
    arrangement[bestPlacement[0]][bestPlacement[1]] = person




from Utils.ValueCalc import calcTable

arrangement = []

def setArrangement(arrangementSize):
    global arrangement
    arrangement = [[0,0,0,0,0,0,0,0]]*arrangementSize
def randomGreedy(input):
    import random
    random.random(len(input))
def placeGreedy(person):
    global arrangement
    bestImprovement
    for i in range(len(arrangement)):
        for j in range(len(arrangement[i])):
            if(arrangement[i][j] != 0):
            preValue = calcTable(arrangement[i])
            arrangement[i][j] = person
            postValue = calcTable(arrangement[i])



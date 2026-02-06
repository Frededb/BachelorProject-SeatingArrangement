from Utils.ValueCalc import calcTable
import math

from Utils.reader import emptyPerson

arrangement = []

def newArrangement(arrangementSize):
    global arrangement
    #sets up the arrangement 2d array based on input size
    arrangement = [[emptyPerson] * 8 for _ in range(math.ceil(arrangementSize/8))]

#only takes preferences and avoidances into account. Returns a sorted list of people from most to least influential
def makeInfluenceList(people):
    name_to_person = {p.name: p for p in people}
    d = {p: 0 for p in people}
    for personA in people:
        for name in personA.preferences:
            personB = name_to_person.get(name)
            if personB.name != "Empty":
                continue
            d[personA] += 10
            d[personB] += 10
        for name in personA.avoidances:
            personB = name_to_person.get(name)
            if personB.name != "Empty":
                continue
            d[personA] += 10
            d[personB] += 10
    return sorted(d, key=d.get, reverse=True)


def influenceListGreedy(input):
    newArrangement(len(input))
    influenceList = makeInfluenceList(input)
    for person in influenceList:
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




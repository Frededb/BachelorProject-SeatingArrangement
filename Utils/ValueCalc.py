import math
from queue import PriorityQueue
from Utils.reader import emptyPerson

COORDS_MAP = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (0, 3),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (1, 3)
}
def getDistanceTo(personA, personB):
    global COORDS_MAP
    return math.sqrt((COORDS_MAP[personA][0] - COORDS_MAP[personB][0]) ** 2 + (COORDS_MAP[personA][1] - COORDS_MAP[personB][1]) ** 2)

def calcPerson(table, index):
    # print("Calculating person at index:", index)
    sum = 0
    personA = table[index]
    if personA.name == "Empty":
        return 0.0
    for i in range(len(table)):
        if i == index:
            continue
        personSum = 0
        personB = table[i]
        if personB.name == "Empty":
            continue
        if personA.studyprogram == personB.studyprogram:
            personSum = personSum + 3
        if personA.year == personB.year:
            personSum = personSum + 1
        if personB.name in personA.preferences:
            personSum = personSum + 10
        if personB.name in personA.avoidances:
            personSum = personSum - 10
        sum = sum + (personSum * 1/getDistanceTo(index, i))
    return round(sum, 1)

def calcTable(table):
    peopleValues = []
    for i in range(len(table)):
        peopleValues.append(calcPerson(table, i))
    return (sum(peopleValues), peopleValues)

def calcArrangement(arrangement):
    peopleValues = []
    tableValues = []
    for i in range(len(arrangement)):
        tableValue, table = calcTable(arrangement[i])
        tableValues.append(tableValue)
        peopleValues.append(table)
    return (sum(tableValues), tableValues, peopleValues)

def calcTheoreticalMax(input, tableSize = 8):
    maxValue = 0

    while len(input) < tableSize:
        input = input + [emptyPerson]

    for personA in input:
        pq = PriorityQueue()
        for personB in input:
            personValue = calcPerson([personA, personB], 0)
            pq.put((-personValue, personB))
        top = [pq.get()[1] for _ in range(tableSize - 1)]
        perfectTable = [top[0], personA, top[2], top[5], top[3], top[1], top[4], top[6]]
        maxValue = maxValue + calcPerson(perfectTable, 1)
    return maxValue


import math

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

def calcPerson (table, index):
    sum = 0
    personA = table[index]
    for i in range(8):
        if i == index:
            continue
        personSum = 0
        personB = table[i]
        if personA.studyprogram == personB.studyprogram:
            personSum += 3
        if personA.year == personB.year:
            personSum += 1
        if i in personA.preferences.includes(personB):
            personSum += 10
        if i in personA.avoidances.includes(personB):
            personSum -= 10
        sum += personSum * getDistanceTo(index, i)

def calcTable (table):
    total = 0
    for i in range(8):
        total += calcPerson(table, i)
    return total

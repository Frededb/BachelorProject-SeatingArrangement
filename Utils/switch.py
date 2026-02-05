

def switch(arrangement, personA, personB):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]] = arrangement[personB[0]][personB[1]], arrangement[personA[0]][personA[1]]
    return arrangement
import random
from copy import deepcopy

def randomPlacement(input, emptyArrangement):
    rng = random.Random()
    inputCopy = deepcopy(input)
    arrangement = deepcopy(emptyArrangement)
    rng.shuffle(inputCopy)
    index = 0
    for table in arrangement:
        for seatIndex in range(len(table)):
            if index >= len(inputCopy):
                return arrangement
            table[seatIndex] = inputCopy[index]
            index += 1
    return arrangement
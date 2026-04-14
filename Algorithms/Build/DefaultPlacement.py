import math
from copy import deepcopy

from Utils.reader import emptyPerson


def defaultPlacement(input, emptyArrangement):
    arrangement = deepcopy(emptyArrangement)
    index = 0
    for table in arrangement:
        for seatIndex in range(len(table)):
            if index >= len(input):
                return arrangement
            table[seatIndex] = input[index]
            index += 1
    return arrangement



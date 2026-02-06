import math, random
from copy import deepcopy

from Utils.reader import emptyPerson


def randomArrangement(input):
    inputCopy = deepcopy(input)
    arrangement = [[emptyPerson] * 8 for _ in range(math.ceil(len(inputCopy) / 8))]
    random.shuffle(inputCopy)
    for i in range(len(inputCopy)):
        arrangement[i//8][i%8] = inputCopy[i]
    return arrangement
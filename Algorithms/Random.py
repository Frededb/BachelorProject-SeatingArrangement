import math, random
from copy import deepcopy

from Utils.reader import emptyPerson

def randomArrangement(input, seed = None):
    # Use a local RNG seeded with `seed` so we don't change the global random state
    rng = random.Random(seed)
    inputCopy = deepcopy(input)
    arrangement = [[emptyPerson] * 8 for _ in range(math.ceil(len(inputCopy) / 8))]
    # shuffle using the local RNG
    rng.shuffle(inputCopy)
    for i in range(len(inputCopy)):
        arrangement[i//8][i%8] = inputCopy[i]
    return arrangement
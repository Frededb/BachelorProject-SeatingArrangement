import math, random

def randomArrangement(input):
    arrangement = [[None] * 8 for _ in range(math.ceil(len(input) / 8))]
    random.shuffle(input)
    for i in range(len(input)):
        arrangement[i//8][i%8] = input[i]
    return arrangement
def makeArrangement(input):
    global arrangement
    for i in range(len(input)):
        arrangement[i//8][i%8] = input[i]
    return arrangement
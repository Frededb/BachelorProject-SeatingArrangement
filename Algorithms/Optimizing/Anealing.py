import random
import math

from Utils.UtilFunctions import getAllPeople, switch
from Utils.ValueCalc import calcArrangement


def AnealTwoPeople(arrangement, k=1000, seed=None):
    if seed is not None:
        random.seed(seed)
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 2 people
    percents = [[0, 0] for _ in range(10)]
    preValueTotal = calcArrangement(arrangement)[0]
    for i in range(k):
        personA = random.choice(allPeople)
        personB = random.choice(allPeople)
        while personB == personA:
            personB = random.choice(allPeople)

        switch(arrangement, personA, personB)

        postValueTotal = calcArrangement(arrangement)[0]

        #linear
        # T = max(0.01, min(1, 1 - i / k))*120
        #exponential
        T = max(0.01, min(1, math.exp(-5 * i / k)))*120

        diff = postValueTotal - preValueTotal
        P = random.random() < math.exp((diff) / T)
        if postValueTotal < preValueTotal:
            percents[i*10//k][0] += P
        if postValueTotal >= preValueTotal or P:
            preValueTotal = postValueTotal
        else:
            switch(arrangement, personA, personB)
        percents[i*10//k][1] += 1
    print("AnealTwoPeople: " + "".join(["\n" + str(percent[0]/percent[1]*100) + "%" for percent in percents]))
    return arrangement
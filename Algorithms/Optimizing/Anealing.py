import random
import math
import time
from copy import deepcopy

from Utils.UtilFunctions import getAllPeople, switch
from Utils.ValueCalc import calcArrangement


def annealing(arrangement, k=None, seed=None, max_seconds=None):
    rng = random.Random(seed)
    allPeople = getAllPeople(arrangement)
    people_count = len(allPeople)

    # Scale iteration budget by instance size.
    if k is None:
        if people_count <= 30:
            k = 200 * people_count
        elif people_count <= 120:
            k = 150 * people_count
        else:
            k = 100 * people_count
        k = max(2000, k)

    start_time = time.perf_counter()
    #generate all combinations of 2 people
    percents = [[0, 0] for _ in range(10)]
    preValueTotal = calcArrangement(arrangement)[0]
    best_value = preValueTotal
    best_arrangement = deepcopy(arrangement)
    for i in range(k):
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break

        personA = rng.choice(allPeople)
        personB = rng.choice(allPeople)
        while personB == personA:
            personB = rng.choice(allPeople)

        switch(arrangement, personA, personB)

        postValueTotal = calcArrangement(arrangement)[0]

        #linear
        # T = max(0.01, min(1, 1 - i / k))*120
        #exponential
        T = max(0.01, min(1, math.exp(-5 * i / k)))*120

        diff = postValueTotal - preValueTotal
        P = rng.random() < math.exp((diff) / T)
        if postValueTotal < preValueTotal:
            percents[i*10//k][0] += P
        if postValueTotal >= preValueTotal or P:
            preValueTotal = postValueTotal
            if preValueTotal > best_value:
                best_value = preValueTotal
                best_arrangement = deepcopy(arrangement)
        else:
            switch(arrangement, personA, personB)
        percents[i*10//k][1] += 1

    # Keep in-place contract while returning the best state seen within the budget.
    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    # print("AnealTwoPeople: " + "".join(["\n" + str(percent[0]/percent[1]*100) + "%" for percent in percents]))
    return arrangement
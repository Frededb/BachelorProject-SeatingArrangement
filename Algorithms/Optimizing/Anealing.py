import random
import math
import time
from copy import deepcopy

from Utils.UtilFunctions import getAllPeople, switch
from Utils.ValueCalc import calcArrangement, calcTable


def _score_after_swap(arrangement, current_score, person_a, person_b):
    """Return the arrangement score after swapping two people.

    The swap is applied temporarily, only the affected table(s) are rescored,
    and then the swap is undone so the caller's arrangement remains unchanged.
    """
    table_a, table_b = person_a[0], person_b[0]

    if table_a == table_b:
        before = calcTable(arrangement[table_a])[0]
        switch(arrangement, person_a, person_b)
        after = calcTable(arrangement[table_a])[0]
        switch(arrangement, person_a, person_b)
        return current_score - before + after

    before_a = calcTable(arrangement[table_a])[0]
    before_b = calcTable(arrangement[table_b])[0]
    switch(arrangement, person_a, person_b)
    after_a = calcTable(arrangement[table_a])[0]
    after_b = calcTable(arrangement[table_b])[0]
    switch(arrangement, person_a, person_b)
    return current_score - before_a - before_b + after_a + after_b


def annealing(arrangement, k=None, seed=None, max_seconds=None, score_tracker=None):
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
    best_true_score = preValueTotal
    best_arrangement = deepcopy(arrangement)
    if score_tracker is not None:
        score_tracker[0] = max(score_tracker[0], best_value)
    for i in range(k):
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break

        personA = rng.choice(allPeople)
        personB = rng.choice(allPeople)
        while personB == personA:
            personB = rng.choice(allPeople)

        postValueTotal = _score_after_swap(arrangement, preValueTotal, personA, personB)

        #linear
        # T = max(0.01, min(1, 1 - i / k))*120
        #exponential
        T = max(0.01, min(1, math.exp(-5 * i / k)))*120

        diff = postValueTotal - preValueTotal
        P = rng.random() < math.exp((diff) / T)
        if postValueTotal < preValueTotal:
            percents[i*10//k][0] += P
        if postValueTotal >= preValueTotal or P:
            switch(arrangement, personA, personB)
            preValueTotal = postValueTotal
            # Periodically recalculate the true score to correct FP drift from
            # incremental _score_after_swap accumulation.
            # TODO: remove this hack, when it has been solved properly
            if i % 500 == 499:
                preValueTotal = calcArrangement(arrangement)[0]
            if preValueTotal > best_value:
                best_value = preValueTotal
                best_arrangement = deepcopy(arrangement)
                if score_tracker is not None:
                    true_score = calcArrangement(best_arrangement)[0]
                    if true_score > best_true_score:
                        best_true_score = true_score
                        score_tracker[0] = max(score_tracker[0], true_score)
        percents[i*10//k][1] += 1

    # Keep in-place contract while returning the best state seen within the budget.
    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    # print("AnealTwoPeople: " + "".join(["\n" + str(percent[0]/percent[1]*100) + "%" for percent in percents]))
    return arrangement
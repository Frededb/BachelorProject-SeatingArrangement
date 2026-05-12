import random
import math
import time

from Utils.UtilFunctions import getAllPeople, switch
from Utils.ValueCalc import calcArrangement


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
    # Keep a shallow snapshot of the best arrangement (store references to the
    # original Person objects). Using deepcopy here can introduce identity
    # differences which may affect caching or downstream checks — store a
    # shallow copy of each table instead.
    best_arrangement = [list(table) for table in arrangement]
    if score_tracker is not None:
        # Ensure we never decrease the externally-visible best score (only ever increase)
        score_tracker[0] = max(score_tracker[0], best_value)
    # Prevent division edge-cases for user-provided k values.
    safe_k = max(1, k)

    for i in range(k):
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break

        personA = rng.choice(allPeople)
        personB = rng.choice(allPeople)
        while personB == personA:
            personB = rng.choice(allPeople)

        switch(arrangement, personA, personB)
        postValueTotal = calcArrangement(arrangement)[0]

        if max_seconds is not None and max_seconds > 0:
            elapsed = time.perf_counter() - start_time
            progress = min(1.0, max(0.0, elapsed / max_seconds))
        else:
            progress = min(1.0, max(0.0, i / safe_k))

        # Exponential cooling based on normalized progress.
        T = max(0.01, min(1, math.exp(-5 * progress))) * 120

        diff = postValueTotal - preValueTotal
        P = rng.random() < math.exp((diff) / T)
        if postValueTotal < preValueTotal:
            percents[i*10//safe_k][0] += P
        if postValueTotal >= preValueTotal or P:
            preValueTotal = postValueTotal
            if preValueTotal > best_value:
                best_value = preValueTotal
                # Save a shallow copy (lists of the current Person references).
                best_arrangement = [list(table) for table in arrangement]
                if score_tracker is not None:
                    # Only increase the external tracker — use max to avoid regressions
                    score_tracker[0] = max(score_tracker[0], best_value)
        else:
            switch(arrangement, personA, personB)  # revert
        percents[i*10//safe_k][1] += 1

    # Keep in-place contract while returning the best state seen within the budget.
    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    # Sanity-check: ensure the restored arrangement matches the recorded best_value.
    final_score = calcArrangement(arrangement)[0]
    if final_score < best_value:
        # This should not normally happen. As a safe fallback, restore using a
        # fresh shallow copy of the saved best and recompute the final score.
        for table_index in range(len(arrangement)):
            arrangement[table_index][:] = best_arrangement[table_index][:]
        final_score = calcArrangement(arrangement)[0]

    if score_tracker is not None:
        # Do not overwrite with a smaller value; keep the maximum observed score
        score_tracker[0] = max(score_tracker[0], final_score)

    # print("AnealTwoPeople: " + "".join(["\n" + str(percent[0]/percent[1]*100) + "%" for percent in percents]))
    return arrangement
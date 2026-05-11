import time
from copy import deepcopy
from Algorithms.Optimizing.LinearSwitchPeopleSets import LinearSwitchPeopleSets
from Utils.ValueCalc import calcArrangement


def repeatedLinearSwitch(arrangement, v, movableCoords=None, max_seconds=None, score_tracker=None):
    """Run repeated linear switch optimization until convergence or timeout.
    
    Args:
        arrangement: List of tables; each table is a list of Person objects.
        v: Maximum switch size for LinearSwitchPeopleSets.
        movableCoords: Optional list of movable person coordinates.
        max_seconds: Optional wall-clock cap; returns best-so-far when the limit is reached.
    
    Returns:
        The same arrangement object, overwritten with the best state discovered.
    """
    start_time = time.perf_counter()
    best_arrangement = deepcopy(arrangement)
    best_score = calcArrangement(arrangement)[0]
    previous_score = best_score

    if score_tracker is not None:
        score_tracker[0] = best_score

    while True:
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break
        
        # Calculate remaining time budget for this iteration
        remaining_time = None
        if max_seconds is not None:
            elapsed = time.perf_counter() - start_time
            remaining_time = max(0.1, max_seconds - elapsed)  # At least 0.1 seconds to make progress
        
        arrangement = LinearSwitchPeopleSets(arrangement, v, movableCoords, max_seconds=remaining_time, score_tracker=score_tracker)
        score = calcArrangement(arrangement)[0]

        if score > best_score:
            best_score = score
            best_arrangement = deepcopy(arrangement)
            if score_tracker is not None:
                score_tracker[0] = best_score

        if score == previous_score:
            break

        previous_score = score

    # Copy best snapshot back into original arrangement object (in-place contract).
    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    return arrangement


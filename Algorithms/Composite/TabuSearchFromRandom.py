import time

from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.TabuSearch import tabuSearch


def tabuSearchFromRandom(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement = randomPlacement(input, emptyArrangement)

    if max_seconds is None:
        return tabuSearch(arrangement, max_seconds=None, score_tracker=score_tracker)

    start_time = time.perf_counter()

    while True:
        remaining_seconds = max_seconds - (time.perf_counter() - start_time)
        if remaining_seconds <= 0:
            break

        arrangement = tabuSearch(arrangement, max_seconds=remaining_seconds, score_tracker=score_tracker)

    return arrangement
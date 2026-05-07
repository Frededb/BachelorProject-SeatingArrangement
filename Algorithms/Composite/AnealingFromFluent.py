import time

from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Optimizing.Anealing import annealing
FromGrouped

def annealingFromGrouped(input, emptyArrangement, max_seconds=None, score_tracker=None):
    arrangement, _ = fluentGroupsFill(input, emptyArrangement)

    if max_seconds is None:
        return annealing(arrangement, max_seconds=None, score_tracker=score_tracker)

    start_time = time.perf_counter()

    while True:
        remaining_seconds = max_seconds - (time.perf_counter() - start_time)
        if remaining_seconds <= 0:
            break

        arrangement = annealing(arrangement, max_seconds=remaining_seconds, score_tracker=score_tracker)

    return arrangement
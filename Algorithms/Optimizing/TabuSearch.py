"""Tabu search optimizer for seating arrangements.

This module keeps the same in-place optimization style used in the rest of the project:
- The input `arrangement` is mutated during search.
- The best arrangement found is copied back before returning.
"""

import random
import time
from copy import deepcopy

from Utils.UtilFunctions import getAllPeople, switch
from Utils.ValueCalc import calcArrangement, calcTable


def _move_key(person_a, person_b):
    """Return a normalized key so swap(A, B) and swap(B, A) map to the same tabu entry."""
    # Keep ordering deterministic to avoid duplicate tabu keys for the same move.
    return (person_a, person_b) if person_a <= person_b else (person_b, person_a)


def _score_after_swap(arrangement, current_score, person_a, person_b):
    """Estimate the new full-arrangement score if two seats are swapped.

    The function performs the swap temporarily, evaluates only affected table(s), then undoes
    the swap. This is much faster than recalculating every table each time.
    """
    # Extract table indices for both selected seats.
    table_a, table_b = person_a[0], person_b[0]

    # If both seats are on the same table, only that table changes.
    if table_a == table_b:
        # Score of the table before the temporary move.
        before = calcTable(arrangement[table_a])[0]
        # Apply candidate swap.
        switch(arrangement, person_a, person_b)
        # Score of the table after candidate swap.
        after = calcTable(arrangement[table_a])[0]
        # Revert the temporary swap to keep caller state unchanged.
        switch(arrangement, person_a, person_b)
        # Update global score by replacing old table contribution with new one.
        return current_score - before + after

    # If seats are on different tables, exactly two tables are affected.
    # Old contribution from first affected table.
    before_a = calcTable(arrangement[table_a])[0]
    # Old contribution from second affected table.
    before_b = calcTable(arrangement[table_b])[0]
    # Apply candidate swap across tables.
    switch(arrangement, person_a, person_b)
    # New contribution from first affected table.
    after_a = calcTable(arrangement[table_a])[0]
    # New contribution from second affected table.
    after_b = calcTable(arrangement[table_b])[0]
    # Revert temporary swap to preserve caller state.
    switch(arrangement, person_a, person_b)
    # Replace old contributions with new contributions in the global score.
    return current_score - before_a - before_b + after_a + after_b


def _sample_pairs(rng, seat_indices, neighborhood_size):
    """Sample unique seat pairs to build a neighborhood for one search iteration."""
    # Number of occupied seat positions available for swap selection.
    seat_count = len(seat_indices)
    # Theoretical maximum number of unique unordered pairs.
    max_pairs = seat_count * (seat_count - 1) // 2
    # Never sample more than possible.
    sample_count = min(neighborhood_size, max_pairs)

    # No pairs can be generated when sample size is zero.
    if sample_count <= 0:
        return []

    # For small complete neighborhoods, generate all pairs directly.
    if sample_count == max_pairs and max_pairs <= 5000:
        # Container for exhaustive pair list.
        pairs = []
        # Outer index of pair.
        for i in range(seat_count):
            # Inner index starts at i+1 to avoid duplicates and self-pairs.
            for j in range(i + 1, seat_count):
                # Store actual seat coordinates, not integer indices.
                pairs.append((seat_indices[i], seat_indices[j]))
        return pairs

    # Track already sampled index pairs to keep sampling unique.
    seen = set()
    # Store sampled coordinate pairs.
    pairs = []
    # Keep sampling until the requested neighborhood size is reached.
    while len(pairs) < sample_count:
        # Pick two distinct seat indices uniformly at random.
        i, j = rng.sample(range(seat_count), 2)
        # Canonical ordering avoids treating (j, i) as a new pair.
        if i > j:
            i, j = j, i
        # Skip duplicates.
        if (i, j) in seen:
            continue
        # Mark pair as used.
        seen.add((i, j))
        # Save as coordinate tuples used by `switch`.
        pairs.append((seat_indices[i], seat_indices[j]))
    return pairs


def tabuSearch(
    arrangement,
    iterations=None,
    tabu_tenure=None,
    neighborhood_size=None,
    max_no_improve=None,
    seed=None,
    max_seconds=None,
    score_tracker=None,
):
    """Run tabu search using swap moves and return the best arrangement found.

    Args:
        arrangement: List of tables; each table is a list of Person objects.
        iterations: Maximum number of tabu iterations. If None, derived from dataset size.
        tabu_tenure: Number of iterations a chosen move remains tabu. If None, derived from size.
        neighborhood_size: Number of candidate swap moves sampled per iteration. If None, derived from size.
        max_no_improve: Early-stop threshold for consecutive non-improving iterations. If None, derived from size.
        seed: Optional deterministic seed for reproducible neighborhood sampling.
        max_seconds: Optional wall-clock cap; returns best-so-far when the limit is reached.

    Returns:
        The same arrangement object, overwritten with the best state discovered.
    """
    # Local RNG keeps reproducibility isolated from global random state.
    rng = random.Random(seed)
    # Seat coordinates used for generating swap candidates.
    seat_indices = getAllPeople(arrangement)
    seat_count = len(seat_indices)
    max_pairs = seat_count * (seat_count - 1) // 2

    # Scale defaults with dataset size so one setting works across small and large instances.
    if tabu_tenure is None:
        tabu_tenure = max(7, min(60, int(round(0.08 * seat_count))))
    if neighborhood_size is None:
        neighborhood_size = min(max_pairs, max(20, 10 * seat_count))
    if max_no_improve is None:
        max_no_improve = max(50, 2 * seat_count)
    if iterations is None:
        iterations = max(2000, 120 * seat_count)

    start_time = time.perf_counter()

    # Starting arrangement score.
    current_score = calcArrangement(arrangement)[0]
    # Best objective value seen so far.
    best_score = current_score
    # Snapshot of the best arrangement for final restoration.
    best_arrangement = deepcopy(arrangement)

    if score_tracker is not None:
        score_tracker[0] = max(score_tracker[0], best_score)

    # Map: move_key -> iteration until which the move stays tabu.
    tabu_until = {}
    # Counter for plateau-based early stopping.
    no_improve = 0

    # Main tabu loop.
    for iteration in range(1, iterations + 1):
        if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
            break

        # Best admissible move in this iteration.
        best_move = None
        # Best resulting score among evaluated candidate moves.
        best_move_score = float("-inf")

        # Evaluate a sampled neighborhood of swaps.
        for person_a, person_b in _sample_pairs(rng, seat_indices, neighborhood_size):
            if max_seconds is not None and (time.perf_counter() - start_time) >= max_seconds:
                break

            # Normalize move identity for tabu lookup.
            move = _move_key(person_a, person_b)
            # A move is tabu while its expiry is in the future.
            is_tabu = tabu_until.get(move, 0) > iteration

            # Compute candidate score by local table-delta evaluation.
            candidate_score = _score_after_swap(arrangement, current_score, person_a, person_b)
            # Aspiration rule: allow tabu move only if it beats global best score.
            if is_tabu and candidate_score <= best_score:
                continue

            # Keep the highest-scoring admissible move.
            if candidate_score > best_move_score:
                best_move = (person_a, person_b, move)
                best_move_score = candidate_score

        # Stop if no admissible move exists.
        if best_move is None:
            break

        # Unpack selected move.
        person_a, person_b, move = best_move
        # Apply selected move permanently for this iteration.
        switch(arrangement, person_a, person_b)
        # Update current objective to chosen move score.
        current_score = best_move_score
        # Mark move tabu for the next `tabu_tenure` iterations.
        tabu_until[move] = iteration + tabu_tenure

        # Track best-ever solution.
        if current_score > best_score:
            # New global best value.
            best_score = current_score
            # New global best state snapshot.
            best_arrangement = deepcopy(arrangement)
            # Reset plateau counter after improvement.
            no_improve = 0
            if score_tracker is not None:
                score_tracker[0] = max(score_tracker[0], best_score)
        else:
            # Count non-improving iterations.
            no_improve += 1

        # Early-stop on long plateau.
        if no_improve >= max_no_improve:
            break

        # Periodically prune expired tabu entries to bound dictionary growth.
        if iteration % 50 == 0:
            tabu_until = {k: v for k, v in tabu_until.items() if v > iteration}

    # Copy best snapshot back into original arrangement object (in-place contract).
    for table_index in range(len(arrangement)):
        arrangement[table_index][:] = best_arrangement[table_index][:]

    return arrangement

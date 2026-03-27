from Algorithms.Optimizing.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets, linearSwitch4PeopleEachTable
from Utils.ValueCalc import calcArrangement
from graph.graph import splitGroupsByMaxSize, makeGraphFromInput


def _empty_seat_indexes(table):
    return [i for i, seat in enumerate(table) if seat.name == "Empty"]


def _pick_highest_scoring_group(groups, emptyArrangement):
    best_group = None
    best_table = None
    best_empty_indexes = None
    best_score = float("-inf")
    best_tiebreak = None
    best_names = None

    for raw_group in groups:
        group = list(raw_group)
        table_index, table, empty_indexes = _pick_best_fit_table(emptyArrangement, len(group))
        if table is None:
            continue

        # Evaluate this exact next move and keep the group that yields max score.
        candidate_arrangement = [list(t) for t in emptyArrangement]
        for seat_index, person in zip(empty_indexes, group):
            candidate_arrangement[table_index][seat_index] = person

        score = calcArrangement(candidate_arrangement)[0]
        leftover_seats = len(empty_indexes) - len(group)
        tiebreak = (
            -leftover_seats,
            len(group),
        )
        names = tuple(sorted(person.name for person in group))

        if (
            score > best_score
            or (score == best_score and (best_tiebreak is None or tiebreak > best_tiebreak))
            or (score == best_score and tiebreak == best_tiebreak and (best_names is None or names < best_names))
        ):
            best_group = group
            best_table = table
            best_empty_indexes = empty_indexes
            best_score = score
            best_tiebreak = tiebreak
            best_names = names

    return best_group, best_table, best_empty_indexes


def _pick_best_fit_table(emptyArrangement, groupSize):
    best = None
    for table_index, table in enumerate(emptyArrangement):
        empty_indexes = _empty_seat_indexes(table)
        empty_count = len(empty_indexes)
        if empty_count < groupSize:
            continue

        candidate_key = (empty_count, len(table), table_index)
        if best is None or candidate_key < best[0]:
            best = (candidate_key, table, empty_indexes)

    if best is None:
        return None, None, None

    return best[0][2], best[1], best[2]

def fillEmptyArrangementWithFluentGroups(input, emptyArrangement):
    remainingPeople = list(input)
    protectedNames = set()

    while len(remainingPeople) > 0:
        table_capacities = [len(_empty_seat_indexes(table)) for table in emptyArrangement]
        maxGroupSize = max(table_capacities)
        if maxGroupSize == 0:
            break

        g = makeGraphFromInput(remainingPeople)
        splittedGroups = splitGroupsByMaxSize(g, remainingPeople, maxGroupSize)
        bestGroup, table, emptySeatIndexes = _pick_highest_scoring_group(splittedGroups, emptyArrangement)
        if table is None:
            raise RuntimeError("No table can fit selected group. Check splitGroupsByMaxSize constraints.")

        print("current table: ", table)

        print("best group: ", bestGroup)

        for seatIndex, person in zip(emptySeatIndexes, bestGroup):
            table[seatIndex] = person

        print("new table: ", table)

        print("------------")

        if len(bestGroup) >= 3:
            for person in bestGroup:
                protectedNames.add(person.name)

        seatedNames = {person.name for person in bestGroup}
        remainingPeople = [person for person in remainingPeople if person.name not in seatedNames]

    emptyArrangement = linearSwitch4PeopleEachTable(emptyArrangement)
    print("score after first bruteforce: ", calcArrangement(emptyArrangement)[0])

    movableCoords = [
        (tableIndex, seatIndex)
        for tableIndex, table in enumerate(emptyArrangement)
        for seatIndex, person in enumerate(table)
        if person.name not in protectedNames
    ]

    emptyArrangement = LinearSwitch4PeopleSets(emptyArrangement, movableCoords)
    print("score after linear switch4people: ", calcArrangement(emptyArrangement)[0])

    return emptyArrangement
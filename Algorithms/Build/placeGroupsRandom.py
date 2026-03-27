from random import Random

from Algorithms.Build.placeGroups import countEmptySeats
from Utils.reader import emptyPerson


def placeGroupsRandom(emptyArrangement, groups, seed=None):
    rng = Random(seed) if seed is not None else Random()
    # sort groups by size
    groups.sort(key=lambda x: len(x), reverse=True)
    # sort emptyTables by number of seats
    emptyArrangement.sort(key=lambda x: len(x))


    #RANDOMLY place the groups
    for group in groups:
        remaining = list(group)

        if len(emptyArrangement) == 0:
            raise ValueError("Cannot place groups: arrangement has no tables")

        randomNumber = rng.randrange(len(emptyArrangement))
        # Start at a random index, then wrap to cover all tables.
        orderedTables = emptyArrangement[randomNumber:] + list(reversed(emptyArrangement[:randomNumber]))

        # Prefer keeping a whole group on one table when possible.
        for table in orderedTables:
            if len(remaining) <= countEmptySeats(table):
                for person in remaining:
                    table[table.index(emptyPerson)] = person
                remaining = []
                break

        # If no single table can fit the whole group, start with the table that
        # currently has the most empty seats, then continue with the rest.
        if len(remaining) > 0:
            splitTables = sorted(orderedTables, key=countEmptySeats, reverse=True)
            for table in splitTables:
                while len(remaining) > 0 and countEmptySeats(table) > 0:
                    table[table.index(emptyPerson)] = remaining.pop()
                if len(remaining) == 0:
                    break

        # Never silently lose people.
        if len(remaining) > 0:
            raise ValueError(f"Not enough empty seats to place all group members. Unplaced: {len(remaining)}")

    return emptyArrangement
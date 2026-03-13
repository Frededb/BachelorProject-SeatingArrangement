from random import random

from Algorithms.FromGroups import countEmptySeats
from Utils.reader import emptyPerson


def placeGroupsRandom(emptyArrangement, groups):
    # sort groups by size
    groups.sort(key=lambda x: len(x), reverse=True)
    # sort emptyTables by number of seats
    emptyArrangement.sort(key=lambda x: len(x))


    #RANDOMLY place the groups
    for group in groups:
        remaining = list(group)

        if len(emptyArrangement) == 0:
            raise ValueError("Cannot place groups: arrangement has no tables")

        randomNumber = int(random() * len(emptyArrangement))
        # Start at a random index, then wrap to cover all tables.
        orderedTables = emptyArrangement[randomNumber:] + list(reversed(emptyArrangement[:randomNumber]))

        # Prefer keeping a whole group on one table when possible.
        for table in orderedTables:
            if len(remaining) <= countEmptySeats(table):
                for person in remaining:
                    table[table.index(emptyPerson)] = person
                remaining = []
                break

        # If no single table can fit the whole group, spread across all tables.
        if len(remaining) > 0:
            for table in orderedTables:
                while len(remaining) > 0 and countEmptySeats(table) > 0:
                    table[table.index(emptyPerson)] = remaining.pop()
                if len(remaining) == 0:
                    break

        # Never silently lose people.
        if len(remaining) > 0:
            raise ValueError(f"Not enough empty seats to place all group members. Unplaced: {len(remaining)}")

    return emptyArrangement
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
        group = list(group)
        randomNumber = int(random() * len(emptyArrangement))
        for table in emptyArrangement[randomNumber:]:
            if len(group) <= countEmptySeats(table):
                for person in group:
                    table[table.index(emptyPerson)] = person
                break
        else:
            for table in reversed(emptyArrangement[:randomNumber]):
                for _ in range(countEmptySeats(table)):
                    if len(group) == 0:
                        break
                    table[table.index(emptyPerson)] = group.pop()
                if len(group) == 0:
                    break
    return emptyArrangement
from Utils.reader import emptyPerson


def fromGroups(emptyArrangement, groups):
    #sort groups by size
    groups.sort(key=lambda x: len(x), reverse=True)
    #sort emptyTables by number of seats
    emptyArrangement.sort(key=lambda x: len(x))

    #fill out the tables from smallest to biggest with the closed groups
    for group in groups:
        group = list(group)
        for table in emptyArrangement:
            if len(group) <= countEmptySeats(table):
                for person in group:
                    table[table.index(emptyPerson)] = person
                break
        else:
            for table in reversed(emptyArrangement):
                for _ in range(countEmptySeats(table)):
                    if len(group) == 0:
                        break
                    table[table.index(emptyPerson)] = group.pop()
                if len(group) == 0:
                    break

    return emptyArrangement

def countEmptySeats(table):
    return sum(1 for seat in table if seat == emptyPerson)
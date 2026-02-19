from Algorithms.findClosedGroups import findClosedGroups
from Utils.reader import emptyPerson


def fromClosedGroups(emptyArrangement, input):
    closedGroups = findClosedGroups(input)
    #convert closedGroups to a list
    closedGroups = list(closedGroups)
    #sort closedGroups by size
    closedGroups.sort(key=lambda x: len(x), reverse=True)
    #sort emptyTables by number of seats
    emptyArrangement.sort(key=lambda x: len(x), reverse=True)

    #fill out the tables from left to right with the closed groups
    for group in closedGroups:
        for table in emptyArrangement:
            if len(group) <= countEmptySeats(table):
                for person in group:
                    table[table.index(emptyPerson)] = person
                break

    return emptyArrangement

def countEmptySeats(table):
    return sum(1 for seat in table if seat == emptyPerson)
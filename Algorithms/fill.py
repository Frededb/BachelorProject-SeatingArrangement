from Utils.reader import emptyPerson


def fill(emptyArrangement, people):
    for person in people:
        for table in emptyArrangement:
            if emptyPerson in table:
                table[table.index(emptyPerson)] = person
                break

    return emptyArrangement
from Utils import reader

def getAllPeople(arrangement):
    seat_indices = [(ti, si) for ti, table in enumerate(arrangement) for si in range(len(table))]
    return seat_indices

def switch(arrangement, personA, personB):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]] = arrangement[personB[0]][personB[1]], arrangement[personA[0]][personA[1]]
    return arrangement

def customArrangement(arrangement, personList):
    peopleMap = {person.name: person for table in arrangement for person in table}
    for table in personList:
        for person in table:
            if person not in peopleMap:
                raise ValueError(f"Person {person} not found in arrangement.")
    new_arrangement = [list(map(lambda name: peopleMap[name] or reader.emptyPerson, table)) for table in personList]
    return new_arrangement

    
    
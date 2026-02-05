
def getAllPeople(arrangement):
    seat_indices = [(ti, si) for ti, table in enumerate(arrangement) for si in range(len(table))]
    return seat_indices

def switch(arrangement, personA, personB):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]] = arrangement[personB[0]][personB[1]], arrangement[personA[0]][personA[1]]
    return arrangement

def customArrangement(input, personList):
    inputNames = [person.name for person in input]
    if set(inputNames) != set(personList):
        raise ValueError("Input and personList do not match")
    input = sorted(input, key=lambda x: personList.index(x.name))
    return input # should be converted to arrangement

    
    
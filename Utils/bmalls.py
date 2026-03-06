from math import ceil

from Utils import reader

def getAllPeople(arrangement):
    seat_indices = [(ti, si) for ti, table in enumerate(arrangement) for si in range(len(table))]
    return seat_indices

def switch(arrangement, personA, personB):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]] = arrangement[personB[0]][personB[1]], arrangement[personA[0]][personA[1]]
    return arrangement

def switchPair(arrangement, pairA, pairB):
    arrangement[pairA[1][0]][pairA[1][1]], arrangement[pairB[1][0]][pairB[1][1]] = arrangement[pairB[1][0]][pairB[1][1]], arrangement[pairA[1][0]][pairA[1][1]]
    arrangement[pairA[0][0]][pairA[0][1]], arrangement[pairB[0][0]][pairB[0][1]] = arrangement[pairB[0][0]][pairB[0][1]], arrangement[pairA[0][0]][pairA[0][1]]
    return arrangement

def switchPairBack(arrangement, pairA, pairB):
    arrangement[pairA[0][0]][pairA[0][1]], arrangement[pairB[0][0]][pairB[0][1]] = arrangement[pairB[0][0]][pairB[0][1]], arrangement[pairA[0][0]][pairA[0][1]]
    arrangement[pairA[1][0]][pairA[1][1]], arrangement[pairB[1][0]][pairB[1][1]] = arrangement[pairB[1][0]][pairB[1][1]], arrangement[pairA[1][0]][pairA[1][1]]
    return arrangement

def switch3People(arrangement, personA, personB, personC):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]] = arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]], arrangement[personA[0]][personA[1]]
    return arrangement

def switch3PeopleBack(arrangement, personA, personB, personC):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]] = arrangement[personC[0]][personC[1]], arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]]
    return arrangement

def switch4People(arrangement, personA, personB, personC, personD):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]], arrangement[personD[0]][personD[1]] = arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]], arrangement[personD[0]][personD[1]], arrangement[personA[0]][personA[1]]
    return arrangement

def switch4PeopleBack(arrangement, personA, personB, personC, personD):
    arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]], arrangement[personD[0]][personD[1]] = arrangement[personD[0]][personD[1]], arrangement[personA[0]][personA[1]], arrangement[personB[0]][personB[1]], arrangement[personC[0]][personC[1]]
    return arrangement

def customArrangement(arrangement, personList):
    peopleMap = {person.name: person for table in arrangement for person in table}
    for table in personList:
        for person in table:
            if person not in peopleMap:
                raise ValueError(f"Person {person} not found in arrangement.")
    new_arrangement = [list(map(lambda name: peopleMap[name] or reader.emptyPerson, table)) for table in personList]
    return new_arrangement

def getPersonByName(name, input):
    for person in input:
        if person.name == name:
            return person
    print("Person not found: ", name)
    return None

def getPersonsByName(names, input):
    persons = set()
    for name in names:
        person = getPersonByName(name, input)
        if person is not None:
            persons.add(person)
        else:
            print("Person not found: ", name)
    return persons

def makeEmptyArrangement(n, tableSize):
    from Utils.reader import emptyPerson
    return [[emptyPerson for _ in range(tableSize)] for _ in range(ceil(n/tableSize))]
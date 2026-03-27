import itertools

from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import getAllPeople, switch


def LinearSwitch2PeopleSets(arrangement):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 2 people
    combinations = itertools.combinations(allPeople, 2)
    for personA, personB in combinations:
        preValueTotal = calcArrangement(arrangement)[0]

        switch(arrangement, personA, personB)

        postValueTotal = calcArrangement(arrangement)[0]

        if postValueTotal < preValueTotal:
            switch(arrangement, personA, personB)  # Switch back if no improvementt))
    return arrangement

def LinearSwitch2PeopleRandom(arrangement):
    allPeople = getAllPeople(arrangement)
    for _ in range(int(len(allPeople)**2)):
        personA = random.choice(allPeople)
        personB = random.choice(allPeople)
        while personB == personA:
            personB = random.choice(allPeople)

        preValueTableA = calcTable(arrangement[personA[0]])[0]
        preValueTableB = calcTable(arrangement[personB[0]])[0]
        preValueTotal = preValueTableA + preValueTableB

        switch(arrangement, personA, personB)

        postValueTableA = calcTable(arrangement[personA[0]])[0]
        postValueTableB = calcTable(arrangement[personB[0]])[0]
        postValueTotal = postValueTableA + postValueTableB

        if postValueTotal < preValueTotal:
            switch(arrangement, personA, personB)  # Switch back if no improvement
    return arrangement

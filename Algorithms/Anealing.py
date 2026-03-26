import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import getAllPeople, switch4People, switch4PeopleBack, switch3People, switch3PeopleBack, switch


def AnealTwoPeople(arrangement, k=1000):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 2 people
    combinations = itertools.combinations(allPeople, 2)
    preValueTotal = calcArrangement(arrangement)[0]
    for i in range(k):
        personA, personB = random.choice(list(combinations))

        switch(arrangement, personA, personB)

        postValueTotal = calcArrangement(arrangement)[0]

        T = max(0.01, min(1, 1 - i / k))*100

        if postValueTotal >= preValueTotal or random.random() < math.exp(-(postValueTotal - preValueTotal) / T):
            preValueTotal = postValueTotal
        else:
            switch(arrangement, personA, personB)
    return arrangement
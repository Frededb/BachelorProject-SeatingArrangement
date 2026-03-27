import itertools
import random
import math

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import getAllPeople, switch4People, switch4PeopleBack, switch3People, switch3PeopleBack, switch


def AnealTwoPeople(arrangement, k=1000):
    allPeople = getAllPeople(arrangement)
    #generate all combinations of 2 people
    preValueTotal = calcArrangement(arrangement)[0]
    for i in range(k):
        personA = random.choice(allPeople)
        personB = random.choice(allPeople)
        while personB == personA:
            personB = random.choice(allPeople)

        switch(arrangement, personA, personB)

        postValueTotal = calcArrangement(arrangement)[0]

        T = max(0.01, min(1, 1 - i / k))*100

        P = random.random() < math.exp(-(postValueTotal - preValueTotal) / T)
        if postValueTotal >= preValueTotal or P:
            preValueTotal = postValueTotal
        else:
            switch(arrangement, personA, personB)
    return arrangement
import random
from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import switch, getAllPeople

def randomSwitch(arrangement, N=1000):
    seat_indices = getAllPeople(arrangement)
    current_score, _, _ = calcArrangement(arrangement)
    for i in range(N):
        personA, personB = random.sample(seat_indices, 2)
        switch(arrangement, personA, personB)
        new_score, _, _ = calcArrangement(arrangement)
        if new_score < current_score:
            switch(arrangement, personA, personB)
        else:
            current_score = new_score
    return arrangement

    

    


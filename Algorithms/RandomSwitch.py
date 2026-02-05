import random
from Utils.ValueCalc import calcArrangement
from Utils.bmalls import switch, getAllPeople

# tablearrangement = [[8 * person] * x]

def postOptimize(arrangement):
    seat_indices = getAllPeople(arrangement)
    if len(seat_indices) < 2:
        raise ValueError("Need at least two seats to choose distinct people.")
    current_score, _, _ = calcArrangement(arrangement)
    for i in range(100):
        personA, personB = random.sample(seat_indices, 2)
        switch(arrangement, personA, personB)
        new_score, _, _ = calcArrangement(arrangement)
        if new_score < current_score:
            switch(arrangement, personA, personB)
        else:
            current_score = new_score
    return arrangement

    

    


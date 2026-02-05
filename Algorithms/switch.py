import random
from Utils.ValueCalc import calcArrangement
from Utils.switch import switch

# tablearrangement = [[8 * person] * x]
def switchRandom(arrangement):
    seat_indices = [(ti, si) for ti, table in enumerate(arrangement) for si in range(len(table))]
    if len(seat_indices) < 2:
        raise ValueError("Need at least two seats to choose distinct people.")
    personA, personB = random.sample(seat_indices, 2)
    switch(arrangement, personA, personB)
    return arrangement
    

    


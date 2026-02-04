import random


# tablearrangement = [[8 * person] * x]
def a(arrangement):
    seat_indices = [(ti, si) for ti, table in enumerate(arrangement) for si in range(len(table))]
    if len(seat_indices) < 2:
        raise ValueError("Need at least two seats to choose distinct people.")
    personA, personB = random.sample(seat_indices, 2)
    while personA == personB:
        personA, personB = random.sample(seat_indices, 2)
    print(personA, personB)
    


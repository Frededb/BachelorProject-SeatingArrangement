from itertools import combinations
import math

calculatedTables = {}

def calcPersonUnordered(table, index):
    # print("Calculating person at index:", index)
    sum = 0
    personA = table[index]
    if personA.name == "Empty":
        return 0.0
    for i in range(len(table)):
        if i == index:
            continue
        personSum = 0
        personB = table[i]
        if personB.name == "Empty":
            continue
        if personA.studyprogram == personB.studyprogram:
            personSum = personSum + 3
        if personA.year == personB.year:
            personSum = personSum + 1
        if personB.name in personA.preferences:
            personSum = personSum + 10
        if personB.name in personA.avoidances:
            personSum = personSum - 10
        sum = sum + personSum
    return sum

def calcTableUnordered(table):
    table_hash = hash(tuple(table))
    if table_hash in calculatedTables:
        return calculatedTables[table_hash]
    peopleValues = []
    for i in range(len(table)):
        peopleValues.append(calcPersonUnordered(table, i))
    calculatedTables[table_hash] = (sum(peopleValues), peopleValues)
    return (sum(peopleValues), peopleValues)

def calcArrangementUnordered(arrangement):
    peopleValues = []
    tableValues = []
    for i in range(len(arrangement)):
        tableValue, table = calcTableUnordered(arrangement[i])
        tableValues.append(tableValue)
        peopleValues.append(table)
    return (sum(tableValues), tableValues, peopleValues)

def get_2d_combinations(arrangement):
    # 1. Flatten into a single list
    flat_list = [person for table in arrangement for person in table]

    # 2. Generate all combinations
    for comb in combinations(flat_list,8):
        # 3. Split back into arrangements
        comb_iter = iter(comb)
        new_arrangement = [
            [next(comb_iter) for _ in table] for table in arrangement
        ]
        yield new_arrangement


def bruteForceUnorderedGroups(initialArrangement):
    #here I will generate all combinations of input
    all_arrangements = get_2d_combinations(initialArrangement)
    bestValue = -math.inf
    bestArrangement = -1

    #we go through each and see if they are better than the previous best
    for arrangement in all_arrangements:
        permValue = calcArrangementUnordered(arrangement)[0]

        if permValue > bestValue:
            bestValue = permValue
            bestArrangement = arrangement
    return bestArrangement


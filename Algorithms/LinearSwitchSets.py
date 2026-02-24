import itertools

from Utils.ValueCalc import calcTable, calcArrangement
from Utils.bmalls import switch, getAllPeople


def LinearSwitchSets(arrangement, size, N):
    allPeople = getAllPeople(arrangement)
    print("HEre:", allPeople)
    subsets = list(itertools.combinations(allPeople, size))

    print(f"Generated {len(subsets)} subsets of size {size}")

    # count = 0
    # for group1 in subsets:
    #     for group2 in subsets:
    #         count+=1
    #         if count%1000 == 0:
    #             print(f"Checked {count} combinations")

    # for i in range(N):
    #     for personA in allPeople:
    #         for personB in allPeople:
    #             if personA == personB:
    #                 continue
    #
    #             preValueTableA = calcTable(arrangement[personA[0]])[0]
    #             preValueTableB = calcTable(arrangement[personB[0]])[0]
    #             preValueTotal = preValueTableA + preValueTableB
    #
    #             switch(arrangement, personA, personB)
    #             postValueTableA = calcTable(arrangement[personA[0]])[0]
    #             postValueTableB = calcTable(arrangement[personB[0]])[0]
    #             postValueTotal = postValueTableA + postValueTableB
    #
    #             if postValueTotal < preValueTotal:
    #                 switch(arrangement, personA, personB)  # Switch back if no improvement
    #             # else:
    #             #     print(f"Switched {arrangement[personB[0]][personB[1]].name} and {arrangement[personA[0]][personA[1]].name} for improvement from {preValueTotal} to {postValueTotal}")
    #     print(f"Iteration {i} complete with value: {calcArrangement(arrangement)}")
    return arrangement
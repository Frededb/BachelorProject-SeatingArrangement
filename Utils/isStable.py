import itertools

from Utils.ValueCalc import calcPerson
from Utils.UtilFunctions import getAllPeople, switch
from Utils.printer import printTableWithValues


def isStable(arrangement):
    allPeople = getAllPeople(arrangement)
    count = 0
    combinations = itertools.combinations(allPeople, 2)
    for placement1, placement2 in combinations:
        preValuePersonA = round(calcPerson(arrangement[placement1[0]], placement1[1]), 2)
        preValuePersonB = round(calcPerson(arrangement[placement2[0]], placement2[1]), 2)

        switch(arrangement, placement1, placement2)  # Switch placement1 and placement2

        postValuePersonA = round(calcPerson(arrangement[placement2[0]], placement2[1]), 2)
        postValuePersonB = round(calcPerson(arrangement[placement1[0]], placement1[1]), 2)


        if postValuePersonA > preValuePersonA and postValuePersonB > preValuePersonB:
            count+=1
            print(f"Found instability between {arrangement[placement1[0]][placement1[1]].name} and {arrangement[placement2[0]][placement2[1]].name}")
            print(f"{arrangement[placement2[0]][placement2[1]].name} value: {preValuePersonA} -> {postValuePersonA}")
            print(f"{arrangement[placement1[0]][placement1[1]].name} value: {preValuePersonB} -> {postValuePersonB}")
            printTableWithValues(arrangement[placement1[0]])
            printTableWithValues(arrangement[placement2[0]])
        switch(arrangement, placement1, placement2)  # Switch back to original arrangement

    return count
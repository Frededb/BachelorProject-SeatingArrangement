import path
from Algorithms.FromGroups import fromGroups

from Algorithms.LinearSwitch3PeopleSets import LinearSwitch3PeopleSets
from Algorithms.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets

from Algorithms.DefaultPlacement import defaultPlacement
from Algorithms.LinearSwitch2People import LinearSwitch2People
from Algorithms.LinearSwitch3People import LinearSwitch3People
from Algorithms.LinearSwitch4People import LinearSwitch4People
from Algorithms.Random import randomArrangement
from Algorithms.fill import fill
from Algorithms.findPairs import findPairs
from Algorithms.placeGroupsRandom import placeGroupsRandom
from Utils.isStable import isStable
from Utils.printer import printArrangementWithValues



import reader
import ValueCalc
from Algorithms.BruteForce import bruteForce, bruteForceEachTable
import printer
from Utils.bmalls import customArrangement, makeEmptyArrangement, makeEmptyArrangementFromTableAmount

from Utils.ValueCalc import calcArrangement
import math
import random

import os
import sys

from graph.graph import makeGraphFromInput, print_graph, find_groups, print_groups, splitGroupsByMaxSize

script_dir = os.path.dirname(os.path.abspath(__file__))
input100People = reader.readjson(os.path.join(script_dir, "../Inputs/input100People.json"))
input1Table = reader.readjson(os.path.join(script_dir, "../Inputs/input1Table.json"))
input100PeopleSimple = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleSimple.json"))
input100PeopleMoreRandom = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleMoreRandom.json"))
input100PeopleSemiRandom = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleSemiRandom.json"))
input4People = reader.readjson(os.path.join(script_dir, "../Inputs/input4People.json"))
inputReal = reader.readjson(os.path.join(script_dir, "../Inputs/inputReal.json"))

INPUTS_BY_NAME = {
    "input100People": input100People,
    "input1Table": input1Table,
    "input100PeopleSimple": input100PeopleSimple,
    "input100PeopleMoreRandom": input100PeopleMoreRandom,
    "input100PeopleSemiRandom": input100PeopleSemiRandom,
    "input4People": input4People,
    "inputReal": inputReal,
}

# 6*8+5*6+6*4
emptyArrangementMixed = makeEmptyArrangementFromTableAmount(6, 8) + makeEmptyArrangementFromTableAmount(5, 6) + makeEmptyArrangementFromTableAmount(6, 4)

# input1Table = reader.readjson("../Inputs/input1Table.json")
# input2People = reader.readjson("../Inputs/input2People.json")
# input4People = reader.readjson("../Inputs/input4People.json")
# input6People = reader.readjson("../Inputs/input6People.json")
# input7People = reader.readjson("../Inputs/input7People.json")
# input100People = reader.readjson("../Inputs/input100People.json")

def testcalcPerson(input = input1Table):
    print("lida: ", ValueCalc.calcPerson(input, 0))
def testcalcTable(input = input1Table):
    print("table: ", ValueCalc.calcTable(input))

def testcalcTable2(input = input1Table):
    print("table: ", ValueCalc.calcTable(input))

def testbruteForce(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    value = bruteForce([input1Table])
    print(value, calcArrangement(value))
    printer.printArrangementWithValues(value)

def testRandomGreedy(input = input1Table):
    from Algorithms.RandomGreedy import randomGreedy
    value = randomGreedy(input)
    print("RandomGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testInfluenceListGreedy(input = input1Table):
    from Algorithms.InfluenceListGreedy import influenceListGreedy
    value = influenceListGreedy(input)
    print("InfluenceListGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testDefaultPlacement(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    default = defaultPlacement(input)
    print("DefaultPlacement: ", calcArrangement(default)[0], default, calcArrangement(default))

def testRandom(input = input1Table):
    from Algorithms.Random import randomArrangement
    randomArrangement = randomArrangement(input)
    # print("Random: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))
    printer.printArrangementWithValues(randomArrangement)

def testRepeatedRandom(input = input1Table, N = 100):
    from Algorithms.RepeatedRandom import repeatedRandom
    randomArrangement = repeatedRandom(N, input)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testLinearSwitch2People(arrangement):
    from Algorithms.LinearSwitch2People import LinearSwitch2People

    # run linear switch untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitch2People(arrangement)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best switch: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitchFromClosedgroups(input = input1Table, N = 10):
    from Algorithms.LinearSwitch2People import LinearSwitch2People
    from Algorithms.FromGroups import fromGroups
    emptyArrangement = makeEmptyArrangement(len(input), 8)
    arrangement = fromGroups(emptyArrangement, input)
    optimizedArrangement = LinearSwitch2People(arrangement, N)
    printer.printArrangementWithValues(optimizedArrangement)
    print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))

def testRandomSwitch(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    from Algorithms.RandomSwitch import randomSwitch
    randomArrangement = randomSwitch(arrangement)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testCustomArrangement(input = input1Table, persons = []):
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    arr = customArrangement(arrangement, persons)
    printer.printArrangementWithValues(arr)

def testcalcTheoreticalMax(input = input1Table):
    print("Theoretical max for input100people:", ValueCalc.calcTheoreticalMax(input))

def testbruteForceEachTable(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    arr = bruteForceEachTable(arrangement)
    printer.printArrangementWithValues(arr)

def testFindClosedGroups(input = input1Table):
    from Algorithms.findClosedGroups import findClosedGroups
    result = findClosedGroups(input)
    for group in result:
        print(group)

def testFromClosedGroups(input = input1Table, tableSize = 8):
    from Algorithms.FromGroups import fromGroups
    arrangement = makeEmptyArrangement(len(input), tableSize)
    fromGroups(arrangement, input)

def testFindPairs(input = input1Table):
    result = findPairs(input)
    for pair in result:
        print(pair)

def testLinearSwitchPairs(arrangement, pairs):
    from Algorithms.LinearSwitchPairs import LinearSwitchPairs

    #run linear switch pairs untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitchPairs(arrangement, pairs)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best Pair switch: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitch3People(arrangement):
    from Algorithms.LinearSwitch3People import LinearSwitch3People

    # run linear switch untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitch3People(arrangement)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best switch 3 people: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitch4People(arrangement):
    from Algorithms.LinearSwitch3People import LinearSwitch3People
    # run linear switch untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitch4People(arrangement)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best switch 4 people: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitch4PeopleSets(arrangement):
    # run linear switch untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitch4PeopleSets(arrangement)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best switch 4 people sets: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitch3PeopleSets(arrangement):
    from Algorithms.LinearSwitch3PeopleSets import LinearSwitch3PeopleSets
    # run linear switch untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitch3PeopleSets(arrangement)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best switch 3 people sets: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitch2PeopleSets(arrangement):
    from Algorithms.LinearSwitch2PeopleSets import LinearSwitch2PeopleSets
    # run linear switch untill it dosent improve anymore
    best = calcArrangement(arrangement)[0]
    while True:
        LinearSwitch2PeopleSets(arrangement)
        calcOptimized = calcArrangement(arrangement)[0]
        print("Best switch 2 people sets: ", calcOptimized)
        if best == calcOptimized:
            break
        best = calcOptimized
    return arrangement

def testLinearSwitchCombined(input = input1Table):
    # pairs = findPairs(input)
    arrangement = randomArrangement(input, 69)
    best = calcArrangement(arrangement)[0]
    while True:
        testLinearSwitch4PeopleSets(arrangement)
        testLinearSwitch2People(arrangement)
        testLinearSwitch3PeopleSets(arrangement)

        calcOptimized = calcArrangement(arrangement)[0]

        if best == calcOptimized:
            break
        best = calcOptimized

    printArrangementWithValues(arrangement)

def testLinearSwitchNTimes(input = input1Table, N = 5):
    bestArrangement = randomArrangement(input)
    bestScore = calcArrangement(bestArrangement)[0]

    for i in range(N):
        arrangement = randomArrangement(input)

        testLinearSwitch3PeopleSets(arrangement)

        calcOptimized = calcArrangement(arrangement)[0]
        print(f"iteration {i}: ", calcOptimized)

        if calcOptimized > bestScore:
            bestScore = calcOptimized
            bestArrangement = arrangement

    return bestArrangement

def testGroupsThenSwitch(input = input1Table):
    g = makeGraphFromInput(input)
    groups = find_groups(g, input, weight_threshold=3)
    print(len(groups))
    a = fromGroups(emptyArrangementMixed, groups)
    LinearSwitch4PeopleSets(a)
    printArrangementWithValues(a)

def testGroupsRandomThenSwitch(input = input1Table):
    g = makeGraphFromInput(input)
    groups = find_groups(g, input, weight_threshold=1.4)
    bigGroups = [group for group in groups if len(group) > 2]
    print("Big Groups", len(bigGroups))
    allOther = [group for group in groups if len(group) <= 2]
    print("All Other", len(allOther))
    allOtherList = [person for group in allOther for person in group]

    bestArrangement = None
    bestScore = -math.inf

    worstArrangement = None
    worstScore = math.inf

    for _ in range(10):

        a = placeGroupsRandom(makeEmptyArrangement(len(input), 8), bigGroups)

        a = bruteForceEachTable(a)

        allEmptyCoords = [(tableIndex, seatIndex) for tableIndex in range(len(a)) for seatIndex in range(len(a[tableIndex])) if a[tableIndex][seatIndex].name == "Empty"]

        fill(a, allOtherList)

        LinearSwitch4PeopleSets(a, allEmptyCoords)

        a = bruteForceEachTable(a)

        score = calcArrangement(a)[0]
        print("Score: ", score)
        if score > bestScore:
            bestScore = score
            bestArrangement = a

        if score < worstScore:
            worstScore = score
            worstArrangement = a

    print("Best Score: ", bestScore)
    printArrangementWithValues(bestArrangement)
    print("Worst Score: ", worstScore)
    printArrangementWithValues(worstArrangement)

def _empty_seat_indexes(table):
    return [i for i, seat in enumerate(table) if seat.name == "Empty"]

def _group_cohesion_score(group, graph):
    names = sorted(person.name for person in group)
    if len(names) <= 1:
        return (float("-inf"), len(names), 0.0)

    total_weight = 0.0
    pair_count = 0
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pair_count += 1
            total_weight += graph.get(names[i], {}).get(names[j], 0.0)

    avg_weight = total_weight / pair_count if pair_count > 0 else float("-inf")
    # Prefer stronger internal cohesion first, then larger groups.
    return (avg_weight, len(names), total_weight)

def _pick_most_cohesive_group(groups, graph):
    best_group = None
    best_score = (float("-inf"), float("-inf"), float("-inf"))
    best_names = None

    for raw_group in groups:
        group = list(raw_group)
        score = _group_cohesion_score(group, graph)
        names = tuple(sorted(person.name for person in group))
        if score > best_score or (score == best_score and (best_names is None or names < best_names)):
            best_group = group
            best_score = score
            best_names = names

    return best_group

def _pick_best_fit_table(emptyArrangement, groupSize):
    best = None
    for table_index, table in enumerate(emptyArrangement):
        empty_indexes = _empty_seat_indexes(table)
        empty_count = len(empty_indexes)
        if empty_count < groupSize:
            continue

        candidate_key = (empty_count, len(table), table_index)
        if best is None or candidate_key < best[0]:
            best = (candidate_key, table, empty_indexes)

    if best is None:
        return None, None

    return best[1], best[2]

def fillEmptyArrangementWithFluentGroups(input, emptyArrangement):
    #shuffle the input
    # random.shuffle(input)

    remainingPeople = list(input)
    protectedNames = set()

    while len(remainingPeople) > 0:
        table_capacities = [len(_empty_seat_indexes(table)) for table in emptyArrangement]
        maxGroupSize = max(table_capacities)
        if maxGroupSize == 0:
            break

        g = makeGraphFromInput(remainingPeople)
        splittedGroups = splitGroupsByMaxSize(g, remainingPeople, maxGroupSize)
        bestGroup = _pick_most_cohesive_group(splittedGroups, g)

        table, emptySeatIndexes = _pick_best_fit_table(emptyArrangement, len(bestGroup))
        if table is None:
            raise RuntimeError("No table can fit selected group. Check splitGroupsByMaxSize constraints.")

        print("current table: ", table)

        print("best group: ", bestGroup)

        for seatIndex, person in zip(emptySeatIndexes, bestGroup):
            table[seatIndex] = person

        print("new table: ", table)

        print("------------")

        if len(bestGroup) >= 3:
            for person in bestGroup:
                protectedNames.add(person.name)

        seatedNames = {person.name for person in bestGroup}
        remainingPeople = [person for person in remainingPeople if person.name not in seatedNames]

    emptyArrangement = bruteForceEachTable(emptyArrangement)
    print("score after first bruteforce: ", calcArrangement(emptyArrangement)[0])

    movableCoords = [
        (tableIndex, seatIndex)
        for tableIndex, table in enumerate(emptyArrangement)
        for seatIndex, person in enumerate(table)
        if person.name not in protectedNames
    ]

    emptyArrangement = LinearSwitch4PeopleSets(emptyArrangement)
    print("score after linear switch4people: ", calcArrangement(emptyArrangement)[0])

    emptyArrangement = LinearSwitch4PeopleSets(emptyArrangement)
    print("score after linear switch4people: ", calcArrangement(emptyArrangement)[0])

    emptyArrangement = bruteForceEachTable(emptyArrangement)
    print("score after bruteforce: ", calcArrangement(emptyArrangement)[0])

    return emptyArrangement

def testCreateRandomInput():
    from Utils.createRandomInput import createRandomInput
    randomInput = createRandomInput(cp = 8, cpp = 0.1, ca = 1, n = 100)
    print(randomInput)
    arrangement = testLinearSwitch2PeopleSets(randomArrangement(randomInput, 69))
    printArrangementWithValues(arrangement)

def testAnealing(arrangement):
    from Algorithms.Anealing import AnealTwoPeople
    print("Initial arrangement: {s}", calcArrangement(arrangement)[0])
    optimizedArrangement = AnealTwoPeople(arrangement, k=1000000)
    print("Optimized arrangement: {s}", calcArrangement(optimizedArrangement)[0])
    return optimizedArrangement


if __name__ == "__main__":
    selectedInputName = sys.argv[1] if len(sys.argv) > 1 else "input100People"
    if selectedInputName not in INPUTS_BY_NAME:
        print("Unknown input:", selectedInputName)
        print("Valid inputs:", ", ".join(sorted(INPUTS_BY_NAME.keys())))
        raise SystemExit(1)

    testInput = INPUTS_BY_NAME[selectedInputName]
    print("Using input:", selectedInputName)
    a = testAnealing(defaultPlacement(testInput))

    printArrangementWithValues(a)
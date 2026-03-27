import path

from Algorithms.FluentGroupsThenSwitch import fillEmptyArrangementWithFluentGroups
from Algorithms.FromGroups import fromGroups

from Algorithms.Optimizing.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets
from Algorithms.Random import randomArrangement
from Utils.printer import printArrangementWithValues



import reader
import ValueCalc
from Algorithms.Optimizing.BruteForce import bruteForce, bruteForceEachTable
import printer
from Utils.bmalls import customArrangement, makeEmptyArrangement, makeEmptyArrangementFromTableAmount

from Utils.ValueCalc import calcArrangement

import os
import sys

from graph.graph import makeGraphFromInput, find_groups

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
    from Algorithms.Build.DefaultPlacement import defaultPlacement
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

def testRandomSwitch(input = input1Table):
    from Algorithms.Build.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    from Algorithms.RandomSwitch import randomSwitch
    randomArrangement = randomSwitch(arrangement)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testCustomArrangement(input = input1Table, persons = []):
    from Algorithms.Build.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    arr = customArrangement(arrangement, persons)
    printer.printArrangementWithValues(arr)

def testcalcTheoreticalMax(input = input1Table):
    print("Theoretical max for input100people:", ValueCalc.calcTheoreticalMax(input))

def testbruteForceEachTable(input = input1Table):
    from Algorithms.Build.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    arr = bruteForceEachTable(arrangement)
    printer.printArrangementWithValues(arr)

def testFromClosedGroups(input = input1Table, tableSize = 8):
    from Algorithms.FromGroups import fromGroups
    arrangement = makeEmptyArrangement(len(input), tableSize)
    fromGroups(arrangement, input)

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
    from Algorithms.Optimizing.LinearSwitch3PeopleSets import LinearSwitch3PeopleSets
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
    from Algorithms.Optimizing.LinearSwitch2PeopleSets import LinearSwitch2PeopleSets
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

def testCreateRandomInput():
    from Utils.createRandomInput import createRandomInput
    randomInput = createRandomInput(cp = 8, cpp = 0.1, ca = 1, n = 100)
    print(randomInput)
    arrangement = testLinearSwitch2PeopleSets(randomArrangement(randomInput, 69))
    printArrangementWithValues(arrangement)

if __name__ == "__main__":
    selectedInputName = sys.argv[1] if len(sys.argv) > 1 else "input100People"
    if selectedInputName not in INPUTS_BY_NAME:
        print("Unknown input:", selectedInputName)
        print("Valid inputs:", ", ".join(sorted(INPUTS_BY_NAME.keys())))
        raise SystemExit(1)

    testInput = INPUTS_BY_NAME[selectedInputName]
    print("Using input:", selectedInputName)
    print("Theory Max: ", ValueCalc.calcTheoreticalMax(testInput, 8))
    a = fillEmptyArrangementWithFluentGroups(testInput, makeEmptyArrangement(len(testInput), 8))

    printArrangementWithValues(a)
import os
import sys

# Ensure the project root is importable when this file is run directly.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from Algorithms.Composit.FluentWithSwitch import FluentWithSwitch

from Algorithms.Build.DefaultPlacement import defaultPlacement
from Algorithms.Optimizing.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets
from Algorithms.Build.RandomPlacement import randomArrangement
from Utils.printer import printArrangementWithValues

from Utils import reader
from Utils import ValueCalc
from Algorithms.Optimizing.BruteForce import bruteForce, bruteForceEachTable
from Utils import printer
from Utils.UtilFunctions import customArrangement, makeEmptyArrangement, makeEmptyArrangementFromTableAmount

from Utils.ValueCalc import calcArrangement

script_dir = os.path.dirname(os.path.abspath(__file__))
input100People = reader.readjson(os.path.join(script_dir, "../Inputs/input100People.json"))
input1Table = reader.readjson(os.path.join(script_dir, "../Inputs/input1Table.json"))
input100PeopleSimple = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleSimple.json"))
input100PeopleMoreRandom = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleMoreRandom.json"))
input100PeopleSemiRandom = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleSemiRandom.json"))
input4People = reader.readjson(os.path.join(script_dir, "../Inputs/input4People.json"))
inputReal = reader.readjson(os.path.join(script_dir, "../Inputs/realData/inputReal.json"))
input300 = reader.readjson(os.path.join(script_dir, "../Inputs/input300.json"))
input100NotRandom = reader.readjson(os.path.join(script_dir, "../Inputs/input100NotRandom.json"))

INPUTS_BY_NAME = {
    "input100People": input100People,
    "input1Table": input1Table,
    "input100PeopleSimple": input100PeopleSimple,
    "input100PeopleMoreRandom": input100PeopleMoreRandom,
    "input100PeopleSemiRandom": input100PeopleSemiRandom,
    "input4People": input4People,
    "inputReal": inputReal,
    "input300": input300,
    "input100NotRandom": input100NotRandom,
}

# 6*8+5*6+6*4
emptyArrangementMixed = makeEmptyArrangementFromTableAmount(6, 8) + makeEmptyArrangementFromTableAmount(5, 6) + makeEmptyArrangementFromTableAmount(6, 4)


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
    from Algorithms.Build.RandomGreedy import randomGreedy
    value = randomGreedy(input)
    print("RandomGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testInfluenceListGreedy(input = input1Table):
    from Algorithms.Build.InfluenceListGreedy import influenceListGreedy
    value = influenceListGreedy(input)
    print("InfluenceListGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testDefaultPlacement(input = input1Table):
    from Algorithms.Build.DefaultPlacement import defaultPlacement
    default = defaultPlacement(input)
    print("DefaultPlacement: ", calcArrangement(default)[0], default, calcArrangement(default))

def testRandom(input = input1Table):
    from Algorithms.Build.RandomPlacement import randomArrangement
    randomArrangement = randomArrangement(input)
    # print("Random: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))
    printer.printArrangementWithValues(randomArrangement)

def testRepeatedRandom(input = input1Table, N = 100):
    from Algorithms.Composit.RepeatedRandom import repeatedRandom
    randomArrangement = repeatedRandom(N, input)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testRandomSwitch(input = input1Table):
    from Algorithms.Build.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    from Algorithms.Optimizing.RandomSwitch import randomSwitch
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
    from Algorithms.Build.placeGroups import fromGroups
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

def testCreateRandomInput():
    from Algorithms.Legacy.createRandomInput import createRandomInput
    randomInput = createRandomInput(cp = 8, cpp = 0.1, ca = 1, n = 100)
    print(randomInput)
    arrangement = testLinearSwitch2PeopleSets(randomArrangement(randomInput, 69))
    printArrangementWithValues(arrangement)

if __name__ == "__main__":
    selectedInputName = sys.argv[1] if len(sys.argv) > 1 else "inputReal"
    if selectedInputName not in INPUTS_BY_NAME:
        print("Unknown input:", selectedInputName)
        print("Valid inputs:", ", ".join(sorted(INPUTS_BY_NAME.keys())))
        raise SystemExit(1)

    testInput = INPUTS_BY_NAME[selectedInputName]
    print("Using input:", selectedInputName)
    print("theory max:", ValueCalc.calcTheoreticalMax(testInput))
    a = FluentWithSwitch(testInput, makeEmptyArrangement(len(testInput), 8))

    printArrangementWithValues(a)

    print("========================================")

    printArrangementWithValues(testLinearSwitch2PeopleSets(defaultPlacement(inputReal)))

    # graph = makeGraphFromInput(inputReal)
    # groups = splitGroupsByMaxSize(graph, inputReal, 30)
    # print_groups(groups)
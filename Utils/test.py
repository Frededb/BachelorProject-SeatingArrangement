import path

from Algorithms.LinearSwitch3PeopleSets import LinearSwitch3PeopleSets
from Algorithms.LinearSwitch4PeopleSets import LinearSwitch4PeopleSets

from Algorithms.DefaultPlacement import defaultPlacement
from Algorithms.LinearSwitch2People import LinearSwitch2People
from Algorithms.LinearSwitch3People import LinearSwitch3People
from Algorithms.LinearSwitch4People import LinearSwitch4People
from Algorithms.Random import randomArrangement
from Algorithms.findPairs import findPairs
from Utils.printer import printArrangementWithValues



import reader
import ValueCalc
from Algorithms.BruteForce import bruteForce, bruteForceEachTable
import printer
from Utils.bmalls import customArrangement, makeEmptyArrangement

from Utils.ValueCalc import calcArrangement

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input100People = reader.readjson(os.path.join(script_dir, "../Inputs/input100People.json"))
input1Table = reader.readjson(os.path.join(script_dir, "../Inputs/input1Table.json"))
input100PeopleSimple = reader.readjson(os.path.join(script_dir, "../Inputs/input100PeopleSimple.json"))

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
    from Algorithms.FromClosedGroups import fromClosedGroups
    emptyArrangement = makeEmptyArrangement(len(input), 8)
    arrangement = fromClosedGroups(emptyArrangement, input)
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
    from Algorithms.FromClosedGroups import fromClosedGroups
    arrangement = makeEmptyArrangement(len(input), tableSize)
    fromClosedGroups(arrangement, input)

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

if __name__ == "__main__":
    testLinearSwitchCombined(input100PeopleSimple)
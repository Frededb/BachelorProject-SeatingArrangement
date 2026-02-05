import sys
import os

from Algorithms.switch import switchRandom

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reader
import ValueCalc
from Algorithms.BruteForce import bruteForce
import printer
from Utils.bmalls import customArrangement
import random

random.seed(42)

from Utils.ValueCalc import calcArrangement

input1 = reader.readjson("../Inputs/input1.json")
input2 = reader.readjson("../Inputs/input2.json")
input3 = reader.readjson("../Inputs/input3.json")
input100people = reader.readjson("../Inputs/input100people.json")

def testcalcPerson(input = input1):
    print("lida: ", ValueCalc.calcPerson(input, 0))
def testcalcTable(input = input1):
    print("table: ", ValueCalc.calcTable(input))

def testcalcTable2(input = input1):
    print("table: ", ValueCalc.calcTable(input))

def testbruteForce(input = input1):
    value = bruteForce([input])
    print(value, calcArrangement(value))

def testRandomGreedy(input = input1):
    from Algorithms.RandomGreedy import randomGreedy
    value = randomGreedy(input)
    print("RandomGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testInfluenceListGreedy(input = input1):
    from Algorithms.InfluenceListGreedy import influenceListGreedy
    value = influenceListGreedy(input)
    print("InfluenceListGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testDefaultPlacement(input = input1):
    from Algorithms.DefaultPlacement import defaultPlacement
    default = defaultPlacement(input)
    print("DefaultPlacement: ", calcArrangement(default)[0], default, calcArrangement(default))

def testSwitcher(input = input1):
    from Algorithms.DefaultPlacement import defaultPlacement
    default = defaultPlacement(input)
    switchRandom(default)
    print("After switch:")
    printer.printArrangementWithValues(default)

def testRandom(input = input1):
    from Algorithms.Random import randomArrangement
    randomArrangement = randomArrangement(input)
    print("Random: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testRepeatedRandom(input = input1):
    from Algorithms.RepeatedRandom import repeatedRandom
    randomArrangement = repeatedRandom(100, input)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testLinearSwitch(input = input1):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    LinearSwitch(arrangement)
    printer.printArrangementWithValues(arrangement)

def testOpt(input = input1):
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    print("Before optimization:")
    printer.printArrangementWithValues(arrangement)
    from Algorithms.RandomSwitch import postOptimize
    postOptimize(arrangement)
    print("After optimization:")
    printer.printArrangementWithValues(arrangement)

def testCustomArrangement(input = input1):
    arr = customArrangement(input, ["Lida", "fbuu", "D2D2", "MMMM", "D1D1", "aubu", "joho", "nsio"])
    printer.printArrangementWithValues([arr])
    print(input1)


def testcalcTheoreticalMax(input = input1):
    print("Theoretical max for input100people:", ValueCalc.calcTheoreticalMax(input))

testbruteForce()

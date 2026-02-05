import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reader
import ValueCalc
from Algorithms.BruteForce import bruteForce
import printer
from itertools import permutations
from Algorithms.switch import switchRandom

from Utils.ValueCalc import calcArrangement

input1 = reader.readjson("../Inputs/input1.json")
input2 = reader.readjson("../Inputs/input2.json")
input3 = reader.readjson("../Inputs/input3.json")

def testcalcPerson():
    print("lida: ", ValueCalc.calcPerson(input1, 0))
def testcalcTable():
    print("table: ", ValueCalc.calcTable(input1))

def testcalcTable2():
    print("table: ", ValueCalc.calcTable(input2))

def testbruteForce():
    value = bruteForce(input1)
    print(value, calcArrangement(value))
def testRandomGreedy():
    from Algorithms.RandomGreedy import randomGreedy
    value = randomGreedy(input1)
    print (value)

def testInfluenceListGreedy():
    from Algorithms.InfluenceListGreedy import influenceListGreedy
    value = influenceListGreedy(input1)
    print (value, calcArrangement(value))

def testDefaultPlacement():
    from Algorithms.DefaultPlacement import defaultPlacement
    value = defaultPlacement(input1)
    print(value, calcArrangement(value))


def testSwitcher():
    arrangement = [input1]
    print("Before switch:")
    printer.printArrangementWithValues(arrangement)
    switchRandom(arrangement)
    print("After switch:")
    printer.printArrangementWithValues(arrangement)

def testLinearSwitch():
    from Algorithms.LinearSwitch import LinearSwitch
    arrangement = [input1]
    print("Before switch:")
    printer.printArrangementWithValues(arrangement)
    LinearSwitch(arrangement)
    print("After switch:")
    printer.printArrangementWithValues(arrangement)

testLinearSwitch()
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
input100people = reader.readjson("../Inputs/input100people.json")

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
    value = randomGreedy(input100people)
    print("RandomGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testInfluenceListGreedy():
    from Algorithms.InfluenceListGreedy import influenceListGreedy
    value = influenceListGreedy(input100people)
    print("InfluenceListGreedy: ", calcArrangement(value)[0], value, calcArrangement(value))

def testDefaultPlacement():
    from Algorithms.DefaultPlacement import defaultPlacement
    value = defaultPlacement(input100people)
    print("DefaultPlacement: ", calcArrangement(value)[0], value, calcArrangement(value))


def testSwitcher():
    arrangement = [input1]
    print("Before switch:")
    printer.printArrangementWithValues(arrangement)
    switchRandom(arrangement)
    print("After switch:")
    printer.printArrangementWithValues(arrangement)

def testRandom():
    from Algorithms.Random import randomArrangement
    value = randomArrangement(input100people)
    print("Random: ", calcArrangement(value)[0], value, calcArrangement(value))
def testRepeatedRandom():
    from Algorithms.RepeatedRandom import repeatedRandom
    value = repeatedRandom(100,input100people)
    print("RepeatedRandom: ", calcArrangement(value)[0], value, calcArrangement(value))

testDefaultPlacement()
testInfluenceListGreedy()

testRepeatedRandom()
testRandom()
testRandomGreedy()

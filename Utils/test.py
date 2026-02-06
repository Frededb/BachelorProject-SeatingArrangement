import sys
import os

from Algorithms.switch import switchRandom

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reader
import ValueCalc
from Algorithms.BruteForce import bruteForce
import printer
from Utils.bmalls import customArrangement

from Utils.ValueCalc import calcArrangement

input1Table = reader.readjson("../Inputs/input1Table.json")
input6People = reader.readjson("../Inputs/input6People.json")
input7People = reader.readjson("../Inputs/input7People.json")
input100People = reader.readjson("../Inputs/input100People.json")

def testcalcPerson(input = input1Table):
    print("lida: ", ValueCalc.calcPerson(input, 0))
def testcalcTable(input = input1Table):
    print("table: ", ValueCalc.calcTable(input))

def testbruteForce(input = input1Table):
    value = bruteForce(input)
    print(value, calcArrangement(value))

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

def testSwitcher(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    default = defaultPlacement(input)
    switchRandom(default)
    print("After switch:")
    printer.printArrangementWithValues(default)

def testRandom(input = input1Table):
    from Algorithms.Random import randomArrangement
    randomArrangement = randomArrangement(input)
    print("Random: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testRepeatedRandom(input = input1Table, N = 100):
    from Algorithms.RepeatedRandom import repeatedRandom
    randomArrangement = repeatedRandom(N, input)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testLinearSwitch(input = input1Table):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    LinearSwitch(arrangement)
    printer.printArrangementWithValues(arrangement)

def testOpt(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    print("Before optimization:")
    printer.printArrangementWithValues(arrangement)
    from Algorithms.RandomSwitch import postOptimize
    postOptimize(arrangement)
    print("After optimization:")
    printer.printArrangementWithValues(arrangement)

def testCustomArrangement(input = input1Table):
    arr = customArrangement(input, ["Lida", "fbuu", "D2D2", "MMMM", "D1D1", "aubu", "joho", "nsio"])
    printer.printArrangementWithValues([arr])
    print(input1Table)

def testcalcTheoreticalMax(input = input1Table):
    print("Theoretical max for input100people:", ValueCalc.calcTheoreticalMax(input))
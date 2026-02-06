import sys
import os

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

def testRandom(input = input1Table):
    from Algorithms.Random import randomArrangement
    randomArrangement = randomArrangement(input)
    print("Random: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testRepeatedRandom(input = input1Table, N = 1000000):
    from Algorithms.RepeatedRandom import repeatedRandom
    randomArrangement = repeatedRandom(10000, input)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testLinearSwitch(input = input1Table, N = 10):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.Random import randomArrangement
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    optimizedArrangement = LinearSwitch(arrangement, N)
    print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))

def testLinearSwitchRandom(input = input1Table, N = 10):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.Random import randomArrangement
    arrangement = randomArrangement(input)
    optimizedArrangement = LinearSwitch(arrangement, N)
    print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))

def testLinearSwitchInfluenceList(input = input1Table, N = 10):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.InfluenceListGreedy import influenceListGreedy
    arrangement = influenceListGreedy(input)
    optimizedArrangement = LinearSwitch(arrangement, N)
    print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))

def testRandomSwitch(input = input1Table):
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    from Algorithms.RandomSwitch import randomSwitch
    randomArrangement = randomSwitch(arrangement)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testCustomArrangement(input = input1Table):
    arr = customArrangement(input, ["Lida", "fbuu", "D2D2", "MMMM", "D1D1", "aubu", "joho", "nsio"])
    printer.printArrangementWithValues([arr])
    print(input1Table)


def testcalcTheoreticalMax(input = input1Table):
    print("Theoretical max for input100people:", ValueCalc.calcTheoreticalMax(input))

# testRandom(input100People)
# testRandomGreedy(input100People)
# testInfluenceListGreedy(input100People)
# testDefaultPlacement(input100People)
# testRandomSwitch(input100People)
testRepeatedRandom(input100People)
# testcalcTheoreticalMax(input100People)
# testLinearSwitch(input100People, 1)
# testLinearSwitchRandom(input100People, 1)
# testLinearSwitchInfluenceList(input100People, 1)


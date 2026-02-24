import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reader
import ValueCalc
from Algorithms.BruteForce import bruteForce, bruteForceEachTable
import printer
from Utils.bmalls import customArrangement

from Utils.ValueCalc import calcArrangement

input1Table = reader.readjson("../Inputs/input1Table.json")
input2People = reader.readjson("../Inputs/input2People.json")
input4People = reader.readjson("../Inputs/input4People.json")
input6People = reader.readjson("../Inputs/input6People.json")
input7People = reader.readjson("../Inputs/input7People.json")
input100People = reader.readjson("../Inputs/input100People.json")

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

def testLinearSwitchDefault(input = input1Table, N = 10):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    optimizedArrangement = LinearSwitch(arrangement, N)
    # print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))
    print("LinearSwithchDefault:")
    printer.printArrangementWithValues(optimizedArrangement)

def testLinearSwitchRandom(input = input1Table, N = 10, seed = None):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.Random import randomArrangement
    arrangement = randomArrangement(input, seed)
    optimizedArrangement = LinearSwitch(arrangement, N)
    # print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))
    print("LinearSwithchRandom:")
    printer.printArrangementWithValues(optimizedArrangement)

def testLinearSwitchInfluenceList(input = input1Table, N = 10):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.InfluenceListGreedy import influenceListGreedy
    arrangement = influenceListGreedy(input)
    optimizedArrangement = LinearSwitch(arrangement, N)
    # print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))
    print("LinearSwithchInfluenceList:")
    printer.printArrangementWithValues(optimizedArrangement)

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




# testFindClosedGroups(input100People)
# testLinearSwitchDefault(input100People)
# testLinearSwitchRandom(input100People)
# testLinearSwitchInfluenceList(input100People)

# testCustomArrangement(input100People, [[
#   "GP11",
#   "S5",
#   "GBOB",
#   "G521",
#   "G522",
#   "S8",
#   "G523",
#   "G1A4"], [
#   "GP51",
#   "S2",
#   "GP42",
#   "GP61",
#   "G2A7",
#   "nsio",
#   "GT12",
#   "G1A5"], [
#   "Lida",
#   "GP81",
#   "G511",
#   "S6",
#   "G533",
#   "GT22",
#   "GT32",
#   "G1A8"], [
#   "G4A3",
#   "G4A5",
#   "GP41",
#   "G1A3",
#   "G512",
#   "S4",
#   "G1A2",
#   "G4A1"], [
#   "G3A2",
#   "GT11",
#   "GP32",
#   "G4A2",
#   "GT51",
#   "GP92",
#   "GP22"], [
#   "GT53",
#   "G531",
#   "GP101",
#   "D1D1",
#   "GT52",
#   "G3A9",
#   "GT33"], [
#   "G2A5",
#   "aubu",
#   "G4A4",
#   "G2A3",
#   "G2A6",
#   "G534",
#   "G3A11",
#   "GP102"], [
#   "G4A8",
#   "G2A8",
#   "G513",
#   "GP12",
#   "GP91",
#   "MMMM",
#   "GT23",
#   "G3A12"], [
#   "GP72",
#   "G3A5",
#   "G2A9",
#   "fbuu",
#   "G3A8",
#   "GP71",
#   "G3A4",
#   "G2A4"], [
#   "S1",
#   "GT31",
#   "G4A7",
#   "GP62",
#   "S3",
#   "GT13",
#   "GT21",
#   "G1A1"], [
#   "GP21",
#   "G1A7",
#   "G532",
#   "joho",
#   "GT42",
#   "G2A1",
#   "G3A10",
#   "G3A3"], [
#   "GT41",
#   "S7",
#   "D2D2",
#   "G4A6",
#   "GP52",
#   "GP82",
#   "G3A6",
#   "G3A1"], [
#   "G1A6",
#   "S9",
#   "G3A7",
#   "GT43",
#   "GP31",
#   "G2A2"]])
# testCustomArrangement(input100People, [[
#     "GP11",
#     "S5",
#     "GBOB",
#     "G521",
#     "G522",
#     "S8",
#     "G523",
#     "G1A4"
#     ], [
#     "GP51",
#     "S2",
#     "GP42",
#     "GP61",
#     "G2A7",
#     "nsio",
#     "GT12",
#     "G1A5"
#     ], [
#     "Lida",
#     "GP81",
#     "G511",
#     "S6",
#     "G533",
#     "GT22",
#     "GT32",
#     "G1A8"
#     ], [
#     "G4A3",
#     "G4A5",
#     "GP41",
#     "G1A3",
#     "G512",
#     "S4",
#     "G1A2",
#     "G4A1"
#     ], [
#     "G3A2",
#     "GT11",
#     "GP32",
#     "G4A2",
#     "GT51",
#     "GP92",
#     "GP22"
#     ], [
#     "GT53",
#     "G531",
#     "GP101",
#     "D1D1",
#     "GT52",
#     "G3A9",
#     "GT33"
#     ], [
#     "G2A5",
#     "aubu",
#     "G4A4",
#     "G2A3",
#     "G2A6",
#     "G534",
#     "G3A11",
#     "GP102"
#     ], [
#     "G4A8",
#     "G2A8",
#     "G513",
#     "GP12",
#     "GP91",
#     "MMMM",
#     "GT23",
#     "G3A12"
#     ], [
#     "GP72",
#     "G3A5",
#     "G2A9",
#     "fbuu",
#     "G3A8",
#     "GP71",
#     "G3A4",
#     "G2A4"
#     ], [
#     "S1",
#     "GT31",
#     "G4A7",
#     "GP62",
#     "S3",
#     "GT13",
#     "GT21",
#     "G1A1"
#     ], [
#     "GP21",
#     "G1A7",
#     "G532",
#     "joho",
#     "GT42",
#     "G2A1",
#     "G3A10",
#     "G3A3"
#     ], [
#     "GT41",
#     "S7",
#     "D2D2",
#     "G4A6",
#     "GP52",
#     "GP82",
#     "G3A6",
#     "G3A1"
#     ], [
#     "G1A6",
#     "S9",
#     "G3A7",
#     "GT43",
#     "GP31",
#     "G2A2"
# ]])

# testRandom(input100People)
testbruteForce()


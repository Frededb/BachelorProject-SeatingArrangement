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
    value = bruteForce([input1Table, input2People])
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

def testRepeatedRandom(input = input1Table, N = 100):
    from Algorithms.RepeatedRandom import repeatedRandom
    randomArrangement = repeatedRandom(N, input)
    print("RepeatedRandom: ", calcArrangement(randomArrangement)[0], randomArrangement, calcArrangement(randomArrangement))

def testLinearSwitchDefault(input = input1Table, N = 10):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.DefaultPlacement import defaultPlacement
    arrangement = defaultPlacement(input)
    optimizedArrangement = LinearSwitch(arrangement, N)
    print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))
    printer.printArrangementWithValues(optimizedArrangement)

def testLinearSwitchRandom(input = input1Table, N = 10, seed = None):
    from Algorithms.LinearSwitch import LinearSwitch
    from Algorithms.Random import randomArrangement
    arrangement = randomArrangement(input, seed)
    optimizedArrangement = LinearSwitch(arrangement, N)
    print("LinearSwitch: ", calcArrangement(optimizedArrangement)[0], optimizedArrangement, calcArrangement(optimizedArrangement))
    printer.printArrangementWithValues(optimizedArrangement)

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
    findClosedGroups(input)


before = [["joho", "MMMM", "aubu", "fbuu", "GP02", "GGS5", "nsio", "Lida"], ["G4A6", "G4A2", "G4A1", "G4A8", "G4A3", "G4A4", "G4A5", "G4A7"], ["GS53", "GS52", "GS11", "GS13", "GS51", "G2A2", "G2A7", "GS12"], ["GBOB", "G3A7", "G3A4", "G3A10", "GGS9", "G3A6", "G3A9", "G3A8"], ["G2A5", "G2A4", "G2A1", "G2A8", "GGS6", "G2A9", "G2A6", "G2A3"], ["GP32", "GP31", "GP12", "GP11", "GGS7", "GGS2", "GGS4", "GP01"], ["G1A3", "G1A8", "G1A2", "G1A1", "G1A4", "G1A6", "G1A5", "G1A7"], ["D2D2", "GS41", "GS42", "GP72", "D1D1", "G523", "GS43", "GP71"], ["G3A3", "G3A12", "G3A11", "GP62", "G3A5", "G3A2", "G3A1", "GP61"], ["GS22", "GS23", "GS32", "GS31", "GS21", "GP51", "GS33", "GP52"], ["GP81", "GP21", "GP22", "G521", "GP82", "GGS3", "GP91", "GP92"], ["G534", "G531", "G512", "G522", "G532", "G513", "G533", "G511"], ["Empty", "Empty", "GP41", "GP42", "Empty", "Empty", "S1", "GGS8"]]
after =  [["GP01", "MMMM", "aubu", "fbuu", "GP02", "GGS5", "nsio", "Lida"], ["G4A6", "G4A2", "G4A1", "G4A8", "G4A3", "G4A4", "G4A5", "G4A7"], ["GS53", "GS52", "GS11", "GS13", "GS51", "G2A2", "G2A7", "GS12"], ["GBOB", "G3A7", "G3A4", "G3A10", "GGS9", "G3A6", "G3A9", "G3A8"], ["G2A5", "G2A4", "G2A1", "G2A8", "GGS6", "G2A9", "G2A6", "G2A3"], ["GP32", "GP31", "GP12", "GP11", "GGS7", "GGS2", "GGS4", "joho"], ["G1A3", "G1A8", "G1A2", "G1A1", "G1A4", "G1A6", "G1A5", "G1A7"], ["D2D2", "GS41", "GS42", "GP72", "D1D1", "G523", "GS43", "GP71"], ["G3A3", "G3A12", "G3A11", "GP62", "G3A5", "G3A2", "G3A1", "GP61"], ["GS22", "GS23", "GS32", "GS31", "GS21", "GP51", "GS33", "GP52"], ["GP81", "GP21", "GP22", "G521", "GP82", "GGS3", "GP91", "GP92"], ["G534", "G531", "G512", "G522", "G532", "G513", "G533", "G511"], ["Empty", "Empty", "GP41", "GP42", "Empty", "Empty", "S1", "GGS8"]]
onetable = [["GP21", "GT53", "GT52", "GT51", "GP22", "G523", "G4A2", "GBOB"]]
onetable2 = [["GP21", "GT53", "GT52", "G523", "GP22", "GT51", "G4A2", "GBOB"]]

# testCustomArrangement(input100People, before)
# testCustomArrangement(input100People, after)
# testCustomArrangement(input100People, onetable)
# testCustomArrangement(input100People, onetable2)
# testLinearSwitchRandom(input100People, 2, 69)
# testbruteForceEachTable()

testFindClosedGroups(input100People)
import reader
import ValueCalc
import printer
from BruteForcePy.BruteForce import bruteForce
from itertools import permutations

from Utils.ValueCalc import calcArrangement

input1 = reader.readjson("../reader/input1.json")
input2 = reader.readjson("../reader/input2.json")
input3 = reader.readjson("../reader/input3.json")

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
    from RandomGreedy.RandomGreedy import randomGreedy
    value = randomGreedy(input1)
    print (value)

def testInfluenceListGreedy():
    from InfluenceListGreedy.InfluenceListGreedy import influenceListGreedy
    value = influenceListGreedy(input1)
    print (value, calcArrangement(value))

#testRandomGreedy()
testInfluenceListGreedy()

import reader
import ValueCalc
import printer

table = reader.readjson("../reader/input1.json")
# print("lida: ", ValueCalc.calcPerson(table, 0))
# print("table: ", ValueCalc.calcTable(table))
# print(ValueCalc.calcArrangement([table]))
printer.printArrangementWithValues([table, table])

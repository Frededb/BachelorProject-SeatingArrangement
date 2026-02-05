import reader
import ValueCalc

def printTable(table):
    print(str(table[0:4]))
    print("┌──────────────────────┐\n└──────────────────────┘")
    print(str(table[4:8]))

def printTableWithValues(table):
    tableValue, peopleValues = ValueCalc.calcTable(table)
    return __printTableWithValues__(table, tableValue, peopleValues)

def __printTableWithValues__(table, tableValue, peopleValues):
    print(''.join(f'{str(v):^8}' for v in table[0:len(table)//2]))
    print("┌────────────────────────────────┐")
    print('│' + ''.join(f'{v:^8}' for v in peopleValues[0:len(table)//2]) + '│')
    print('│{: ^32}│'.format(str(tableValue)))
    print('│' + ''.join(f'{v:^8}' for v in peopleValues[len(table)//2:len(table)]) + '│')
    print("└────────────────────────────────┘")
    print(''.join(f'{str(v):^8}' for v in table[len(table)//2:len(table)]))

def printArrangementWithValues(arrangement):
    totalValue, tableValues, peopleValues = ValueCalc.calcArrangement(arrangement)
    print("=========================")
    for tableIndex in range(len(arrangement)):
        print()
        __printTableWithValues__(arrangement[tableIndex], tableValues[tableIndex], peopleValues[tableIndex])
    print("total value:", totalValue)
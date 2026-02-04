import reader

def printTable(table):
    print(str(table[0:4]))
    print("┌──────────────────────┐\n└──────────────────────┘")
    print(str(table[4:8]))

printTable(reader.readjson("../reader/input1.json"))
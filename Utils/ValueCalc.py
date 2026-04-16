import math
from queue import PriorityQueue
from Utils.reader import emptyPerson

calculatedTables = {}


def _normalize_kind(value):
    return str(value).strip().lower() if value is not None else ""


def _weight_value(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def getDistanceTo(table, personA, personB):
    width = len(table)//2
    personACoords = (personA//width, personA%width)
    personBCoords = (personB//width, personB%width)
    return math.sqrt((personACoords[0] - personBCoords[0]) ** 2 + (personACoords[1] - personBCoords[1]) ** 2)

def calcPerson(table, index):
    # print("Calculating person at index:", index)
    sum = 0
    personA = table[index]
    if getattr(personA, "id", "") == "Empty":
        return 0.0

    atribute_set = getattr(personA, "atribute_set", [])
    attributes_a = getattr(personA, "attributes", [])
    for i in range(len(table)):
        if i == index:
            continue
        personSum = 0
        personB = table[i]
        if getattr(personB, "id", "") == "Empty":
            continue

        attributes_b = getattr(personB, "attributes", [])
        for attr_index, attr_meta in enumerate(atribute_set):
            if attr_index >= len(attributes_a):
                continue

            values_a = attributes_a[attr_index]
            values_b = attributes_b[attr_index] if attr_index < len(attributes_b) else []
            if not isinstance(values_a, list):
                continue
            if not isinstance(values_b, list):
                values_b = []

            weight = _weight_value(attr_meta.get("weight") if isinstance(attr_meta, dict) else 0)
            kind = _normalize_kind(attr_meta.get("kind") if isinstance(attr_meta, dict) else "")

            if kind in {"prefence", "preference"}:
                if personB.id in values_a:
                    personSum += weight
            elif kind in {"traits", "trait"}:
                shared_traits = set(values_a).intersection(values_b)
                personSum += weight * len(shared_traits)

        sum = sum + (personSum * 1/getDistanceTo(table, index, i))
    return sum

def calcTable(table):
    table_hash = hash(tuple(table))
    if table_hash in calculatedTables:
        return calculatedTables[table_hash]
    peopleValues = []
    for i in range(len(table)):
        peopleValues.append(calcPerson(table, i))
    calculatedTables[table_hash] = (sum(peopleValues), peopleValues)
    return (sum(peopleValues), peopleValues)

def calcArrangement(arrangement):
    peopleValues = []
    tableValues = []
    for i in range(len(arrangement)):
        tableValue, table = calcTable(arrangement[i])
        tableValues.append(tableValue)
        peopleValues.append(table)
    return round(sum(tableValues), 2), tableValues, peopleValues

def calcTheoreticalMax(input, tableSize = 8):
    maxValue = 0

    while len(input) < tableSize:
        input = input + [emptyPerson]

    for personA in input:
        pq = PriorityQueue()
        for personB in input:
            personValue = calcPerson([personA, personB], 0)
            pq.put((-personValue, personB))
        top = [pq.get()[1] for _ in range(tableSize - 1)]
        perfectTable = [top[0], personA, top[2], top[5], top[3], top[1], top[4], top[6]]
        maxValue = maxValue + calcPerson(perfectTable, 1)
    return maxValue


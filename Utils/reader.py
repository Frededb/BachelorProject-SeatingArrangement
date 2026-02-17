import json
from Person import Person

def readjson(file):
    people = []

    with open(file) as jsonfile:
        reader = json.load(jsonfile)

        for row in reader:
            #Convert preferences and avoidances to sets for easier handling
            row['preferences'] = set(row.get('preferences', []))
            row['avoidances'] = set(row.get('avoidances', []))
            people.append(Person(**row))

    return people

emptyPerson = Person("Empty", "None", -1, set(), set())

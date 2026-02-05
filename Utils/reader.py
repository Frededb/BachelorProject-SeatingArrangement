import json
from Person import Person

def readjson(file):
    people = []

    with open(file) as jsonfile:
        reader = json.load(jsonfile)

        for row in reader:
            people.append(Person(**row))

    return people

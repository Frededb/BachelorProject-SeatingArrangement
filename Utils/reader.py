import json
import Person
Person = Person.Person

def readjson(file):
    people = []

    with open(file) as jsonfile:
        reader = json.load(jsonfile)

        for row in reader:
            people.append(Person(**row))

    return people
            

read = readjson("../reader/input1.json")
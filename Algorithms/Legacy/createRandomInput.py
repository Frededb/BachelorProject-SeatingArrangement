from Utils.Person import Person
import random


def createRandomInput(cp, cpp, ca, n):
    people = [Person("P" + str(i), str(random.randint(0, 3)), random.randint(2023, 2026)) for i in range(n)]
    [print(person) for person in people]
    for person in people:
        prefcount = random.randint(0, cp)
        for j in range(prefcount):
            newperson = random.choice(people)
            if newperson == person or newperson in person.preferences:
                continue
            person.preferences.append(newperson)
            print(f"{person} {newperson}")
            if random.random() < cpp:
                newperson.preferences.append(person)
                print(f"{newperson} {person}")
        avoidcount = random.randint(0, ca)
        for j in range(avoidcount):
            newperson = random.choice(people)
            if newperson == person or newperson in person.avoidances or newperson in person.preferences:
                continue
            person.avoidances.append(newperson)
            print(f"{person} {newperson}")
    return people


from Utils.bmalls import getPersonByName


def findClosedGroups(input):
    for person1 in input:
        goal = person1.preferences + [person1.name]
        for prefence in person1.preferences:
            person2 = getPersonByName(prefence, input)
            if not listContainsTheSame(goal, person2.preferences + [person2.name]):
                break
        else:
            print("Closed group found: ", goal)


def listContainsTheSame(list1, list2):
    return set(list1) == set(list2)


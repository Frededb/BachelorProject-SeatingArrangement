from Utils.bmalls import getPersonByName


def findClosedGroups(input):
    inputCopy = input.copy()
    closedGroups = set()
    for person1 in inputCopy:
        pre = person1.preferences.copy()
        person1.preferences.add(person1.name)
        for prefence in pre:
            person2 = getPersonByName(prefence, inputCopy)
            person2.preferences.add(person2.name)
            if not person1.preferences == person2.preferences:
                closedGroups.add(frozenset({person1.name}))
                break
        else:
            closedGroups.add(frozenset(person1.preferences))

    return closedGroups


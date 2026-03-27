from Utils.UtilFunctions import getPersonByName


def findPairs(input):
    inputCopy = input.copy()
    pairs = set()
    for person1 in inputCopy:
        for prefence in person1.preferences:
            person2 = getPersonByName(prefence, inputCopy)
            if prefence in person1.preferences and person1.name in person2.preferences:
                pairs.add(frozenset({person1, person2}))
    return pairs
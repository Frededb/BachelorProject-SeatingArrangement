from Algorithms.Build.RandomGreedy import _placeGreedy

#only takes preferences and avoidances into account. Returns a sorted list of people from most to least influential
def influenceListGreedy(input, emptyArrangement):
    influenceList = _makeInfluenceList(input)
    for person in influenceList:
        _placeGreedy(person, emptyArrangement)
    return emptyArrangement

def _makeInfluenceList(people):
    name_to_person = {p.name: p for p in people}
    d = {p: 0 for p in people}
    for personA in people:
        for name in personA.preferences:
            personB = name_to_person.get(name)
            if personB is None:
                continue
            d[personA] += 10
            d[personB] += 10
        for name in personA.avoidances:
            personB = name_to_person.get(name)
            if personB is None:
                continue
            d[personA] += 10
            d[personB] += 10
    return sorted(d, key=d.get, reverse=True)



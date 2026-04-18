from Algorithms.Build.RandomGreedy import _placeGreedy


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _weighted_links_from_attributes(person):
    pref_links = []
    avoid_links = []

    attributes = getattr(person, "attributes", [])
    attribute_set = getattr(person, "attribute_set", [])
    for index, answers in enumerate(attributes):
        if index >= len(attribute_set) or not isinstance(answers, list):
            continue

        metadata = attribute_set[index] if isinstance(attribute_set[index], dict) else {}
        kind = str(metadata.get("kind", "")).strip().lower()
        if kind not in {"prefence", "preference"}:
            continue

        weight = _safe_float(metadata.get("weight"), default=0.0)
        magnitude = abs(weight) if weight != 0 else 10.0
        for answer in answers:
            if not isinstance(answer, str) or not answer:
                continue
            if weight < 0:
                avoid_links.append((answer, magnitude))
            else:
                pref_links.append((answer, magnitude))

    return pref_links, avoid_links

#only takes preferences and avoidances into account. Returns a sorted list of people from most to least influential
def influenceListGreedy(input, emptyArrangement):
    influenceList = _makeInfluenceList(input)
    for person in influenceList:
        _placeGreedy(person, emptyArrangement)
    return emptyArrangement

def _makeInfluenceList(people):
    name_to_person = {}
    for person in people:
        if hasattr(person, "name"):
            name_to_person[person.name] = person
        if hasattr(person, "id"):
            name_to_person[person.id] = person

    d = {p: 0 for p in people}
    for personA in people:
        pref_links, avoid_links = _weighted_links_from_attributes(personA)

        if not pref_links:
            pref_links = [(name, 10.0) for name in getattr(personA, "preferences", [])]
        if not avoid_links:
            avoid_links = [(name, 10.0) for name in getattr(personA, "avoidances", [])]

        for name, weight in pref_links:
            personB = name_to_person.get(name)
            if personB is None:
                continue
            d[personA] += weight
            d[personB] += weight
        for name, weight in avoid_links:
            personB = name_to_person.get(name)
            if personB is None:
                continue
            d[personA] += weight
            d[personB] += weight
    return sorted(d, key=lambda person: d[person], reverse=True)



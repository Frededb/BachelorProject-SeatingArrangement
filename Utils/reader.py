import json
from pathlib import Path
try:
    from .Person import Person
except ImportError:
    from Person import Person


def _normalize_kind(value):
    return str(value).strip().lower() if value is not None else ""


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _load_attribute_set_for_people_file(people_file_path: Path, people_payload):
    if isinstance(people_payload, dict) and isinstance(people_payload.get("attribute_set"), list):
        return people_payload["attribute_set"]

    stem = people_file_path.stem
    if "wishes" in stem:
        catalog_candidate = people_file_path.with_name(f"{stem.replace('wishes', 'attribute_set')}{people_file_path.suffix}")
    elif "attributes" in stem:
        catalog_candidate = people_file_path.with_name(
            f"{stem.replace('attributes', 'attribute_set')}{people_file_path.suffix}"
        )
    else:
        catalog_candidate = people_file_path.with_name(f"{stem}attribute_set{people_file_path.suffix}")

    if not catalog_candidate.exists():
        raise ValueError(
            f"Could not find matching attribute_set file for {people_file_path}. Expected {catalog_candidate}."
        )

    with open(catalog_candidate, encoding="utf-8") as jsonfile:
        catalog_payload = json.load(jsonfile)

    attribute_set = catalog_payload.get("attribute_set") if isinstance(catalog_payload, dict) else None
    if not isinstance(attribute_set, list):
        raise ValueError("The attribute_set file must contain an 'attribute_set' list.")
    return attribute_set


def readjson(file):
    people = []

    people_file_path = Path(file)
    with open(people_file_path, encoding="utf-8") as jsonfile:
        payload = json.load(jsonfile)

    if not isinstance(payload, dict):
        raise ValueError("Input JSON must be an object containing a 'people' list.")

    rows = payload.get("people")
    if not isinstance(rows, list):
        raise ValueError("Input JSON must contain a 'people' list.")

    attribute_set = _load_attribute_set_for_people_file(people_file_path, payload)

    for row in rows:
        if not isinstance(row, dict):
            continue

        person_id = row.get("id")
        if not isinstance(person_id, str) or not person_id.strip():
            continue

        attributes = row.get("attributes", [])
        if not isinstance(attributes, list):
            attributes = []

        person = Person(person_id.strip(), attributes=attributes, attribute_set=attribute_set)

        # Keep transitional compatibility fields derived from metadata.
        for index, answers in enumerate(attributes):
            if index >= len(attribute_set) or not isinstance(answers, list):
                continue

            kind = _normalize_kind(attribute_set[index].get("kind"))
            if kind in {"prefence", "preference"}:
                weight = _to_float(attribute_set[index].get("weight"))
                cleaned_answers = {answer for answer in answers if isinstance(answer, str) and answer}
                if weight < 0:
                    person.avoidances.update(cleaned_answers)
                else:
                    person.preferences.update(cleaned_answers)

        people.append(person)

    return people

emptyPerson = Person("Empty", attributes=[], attribute_set=[])

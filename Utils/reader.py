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


def _load_atribute_set_for_people_file(people_file_path: Path, people_payload):
    if isinstance(people_payload, dict) and isinstance(people_payload.get("atribute_set"), list):
        return people_payload["atribute_set"]

    stem = people_file_path.stem
    if "wishes" in stem:
        catalog_candidate = people_file_path.with_name(f"{stem.replace('wishes', 'atribute_set')}{people_file_path.suffix}")
    elif "atributes" in stem:
        catalog_candidate = people_file_path.with_name(
            f"{stem.replace('atributes', 'atribute_set')}{people_file_path.suffix}"
        )
    else:
        catalog_candidate = people_file_path.with_name(f"{stem}atribute_set{people_file_path.suffix}")

    if not catalog_candidate.exists():
        raise ValueError(
            f"Could not find matching atribute_set file for {people_file_path}. Expected {catalog_candidate}."
        )

    with open(catalog_candidate, encoding="utf-8") as jsonfile:
        catalog_payload = json.load(jsonfile)

    atribute_set = catalog_payload.get("atribute_set") if isinstance(catalog_payload, dict) else None
    if not isinstance(atribute_set, list):
        raise ValueError("The atribute_set file must contain an 'atribute_set' list.")
    return atribute_set


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

    atribute_set = _load_atribute_set_for_people_file(people_file_path, payload)

    for row in rows:
        if not isinstance(row, dict):
            continue

        person_id = row.get("id")
        if not isinstance(person_id, str) or not person_id.strip():
            continue

        atributes = row.get("atributes", [])
        if not isinstance(atributes, list):
            atributes = []

        person = Person(person_id.strip(), atributes=atributes, atribute_set=atribute_set)

        # Keep transitional compatibility fields derived from metadata.
        for index, answers in enumerate(atributes):
            if index >= len(atribute_set) or not isinstance(answers, list):
                continue

            kind = _normalize_kind(atribute_set[index].get("kind"))
            if kind in {"prefence", "preference"}:
                weight = _to_float(atribute_set[index].get("weight"))
                cleaned_answers = {answer for answer in answers if isinstance(answer, str) and answer}
                if weight < 0:
                    person.avoidances.update(cleaned_answers)
                else:
                    person.preferences.update(cleaned_answers)

        people.append(person)

    return people

emptyPerson = Person("Empty", atributes=[], atribute_set=[])

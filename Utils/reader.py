import json
from pathlib import Path
from typing import Any
try:
    from .Person import Person
except ImportError:
    from Person import Person

def parsePeople(input_data, attribute_set):
    # Parse people from input data
    people = []
    if isinstance(input_data, dict):
        rows = input_data.get("people", [])
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    person_id = row.get("id")
                    if isinstance(person_id, str) and person_id.strip():
                        attributes = row.get("attributes", [])
                        if not isinstance(attributes, list):
                            attributes = []
                        person = Person(person_id.strip(), attributes=attributes, attribute_set=attribute_set)
                        people.append(person)

    return people

def _load_json_source(source: str | Path | dict[str, Any], label: str) -> dict[str, Any]:
    if isinstance(source, dict):
        return source

    source_path = Path(source)
    if not source_path.exists():
        raise FileNotFoundError(f"{label} file not found: {source_path}")
    with open(source_path, encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError(f"{label} JSON must be an object")
    return loaded


def readPeople(input_file_path, attribute_set_file_path):
    """Load people + attribute set from file paths or in-memory dictionaries."""
    attribute_set_data = _load_json_source(attribute_set_file_path, "Attribute set")
    attribute_set = attribute_set_data.get("attribute_set", []) if isinstance(attribute_set_data, dict) else []

    input_data = _load_json_source(input_file_path, "Input")
    return parsePeople(input_data, attribute_set)


emptyPerson = Person("Empty", attributes=[], attribute_set=[])

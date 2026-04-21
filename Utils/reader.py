import json
from pathlib import Path
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

def readPeople(input_file_path, attribute_set_file_path):
    """Load people input and combine with attribute_set from separate files"""
    from Utils.Person import Person

    input_file_path = Path(input_file_path)
    attribute_set_file_path = Path(attribute_set_file_path)

    if not input_file_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
    if not attribute_set_file_path.exists():
        raise FileNotFoundError(f"Attribute set file not found: {attribute_set_file_path}")

    # Load attribute set first
    with open(attribute_set_file_path, encoding="utf-8") as f:
        attribute_set_data = json.load(f)
    attribute_set = attribute_set_data.get("attribute_set", []) if isinstance(attribute_set_data, dict) else []

    # Load input data
    with open(input_file_path, encoding="utf-8") as f:
        input_data = json.load(f)

    return parse_people(input_data, attribute_set)


emptyPerson = Person("Empty", attributes=[], attribute_set=[])

import os
import sys
import json
from pathlib import Path
from typing import cast



# Ensure the project root is importable when this file is run directly.
PROJECT_ROOT = cast(str, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from Utils.reader import emptyPerson
from Algorithms.Composite.testComposite import testComposite
from Algorithms.Build.DefaultPlacement import defaultPlacement
from Algorithms.Build.InfluenceListGreedy import influenceListGreedy
from Algorithms.Build.RandomGreedy import randomGreedy
from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Composite.Anealing import anealingFromRandom
from Algorithms.Composite.BruteForce import bruteForceFromRandom
from Algorithms.Composite.FluentWithSwitch import FluentWithSwitch
from Algorithms.Composite.LinearSwitch2PeopleSets import linearSwitch2PeopleSetsFromRandom
from Algorithms.Composite.LinearSwitch3PeopleSets import linearSwitch3PeopleSetsFromRandom
from Algorithms.Composite.LinearSwitch4PeopleSets import linearSwitch4PeopleSetsFromRandom
from Algorithms.Composite.RandomSwitch import randomSwitchFromRandom
from Algorithms.Composite.RepeatedRandom import repeatedRandom
from Algorithms.Composite.tabuSearch import tabuSearchFromRandom
from Utils.printer import printArrangementWithValues

from Utils import ValueCalc
from Utils.UtilFunctions import makeEmptyArrangement


def load_input_with_atribute_set(input_file_path, atribute_set_file_path):
    """Load people input and combine with atribute_set from separate files"""
    from Utils.Person import Person

    input_file_path = Path(input_file_path)
    atribute_set_file_path = Path(atribute_set_file_path)

    if not input_file_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
    if not atribute_set_file_path.exists():
        raise FileNotFoundError(f"Atribute set file not found: {atribute_set_file_path}")

    # Load atribute set first
    with open(atribute_set_file_path, encoding="utf-8") as f:
        atribute_set_data = json.load(f)
    atribute_set = atribute_set_data.get("atribute_set", []) if isinstance(atribute_set_data, dict) else []

    # Load input data
    with open(input_file_path, encoding="utf-8") as f:
        input_data = json.load(f)

    # Parse people from input data
    people = []
    if isinstance(input_data, dict):
        rows = input_data.get("people", [])
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    person_id = row.get("id")
                    if isinstance(person_id, str) and person_id.strip():
                        atributes = row.get("atributes", [])
                        if not isinstance(atributes, list):
                            atributes = []
                        person = Person(person_id.strip(), atributes=atributes, atribute_set=atribute_set)
                        people.append(person)

    return people


ALGORITHMS = {
    "defaultPlacement": defaultPlacement,
    "influenceListGreedy": influenceListGreedy,
    "randomGreedy": randomGreedy,
    "randomPlacement": randomPlacement,
    "repeatedRandom": repeatedRandom,
    "FluentWithSwitch": FluentWithSwitch,
    "anealing": anealingFromRandom,
    "bruteForce": bruteForceFromRandom,
    "switch2People": linearSwitch2PeopleSetsFromRandom,
    "switch3People": linearSwitch3PeopleSetsFromRandom,
    "switch4People": linearSwitch4PeopleSetsFromRandom,
    "randomSwitch": randomSwitchFromRandom,
    "tabuSearch": tabuSearchFromRandom,
    "testComposite": testComposite,
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) != 4:
        print("Usage: python test.py <algorithm> <input_file> <atribute_set_file>")
        print("\nAvailable algorithms:")
        for algo in ALGORITHMS:
            print(f"  - {algo}")
        print("\nExample:")
        print("  python test.py FluentWithSwitch ../Inputs/sheetOutput/Test\\ \\(svar\\)input.json ../Inputs/sheetOutput/Test\\ \\(svar\\)atribute_set.json")
        raise SystemExit(1)

    algorithm_name = sys.argv[1]
    input_file = sys.argv[2]
    atribute_set_file = sys.argv[3]

    # Validate algorithm
    if algorithm_name not in ALGORITHMS:
        print(f"Error: Unknown algorithm '{algorithm_name}'")
        print(f"Available algorithms: {', '.join(sorted(ALGORITHMS))}")
        raise SystemExit(1)

    # Load input and atribute set
    try:
        testInput = load_input_with_atribute_set(input_file, atribute_set_file)
    except Exception as e:
        print(f"Error loading input: {e}")
        raise SystemExit(1)

    if not testInput or len(testInput) == 0:
        print(f"Error: Input is empty")
        raise SystemExit(1)

    print(f"Using algorithm: {algorithm_name}")
    print(f"Using input file: {input_file}")
    print(f"Using atribute set: {atribute_set_file}")
    print(f"Number of people: {len(testInput)}")
    print(f"Theory max: {ValueCalc.calcTheoreticalMax(testInput)}")
    print()

    # Create initial arrangement
    initial_arrangement = makeEmptyArrangement(len(testInput), 6)

    # Arrangement with 1 7-seat table, 1 6-seat table, and 2 5-seat tables.
    mixed_arrangement = [
        [emptyPerson] * 7,
        [emptyPerson] * 6,
        [emptyPerson] * 5,
        [emptyPerson] * 5,
    ]

    # Run the algorithm with the shared (input, emptyArrangement) signature
    result_arrangement = ALGORITHMS[algorithm_name](testInput, initial_arrangement)

    printArrangementWithValues(result_arrangement)

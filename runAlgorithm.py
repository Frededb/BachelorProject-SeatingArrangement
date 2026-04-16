import os
import sys
import json
from pathlib import Path
from typing import cast

from Algorithms.Composite.RepeatedLinearSwitch import RepeatedLinearSwitch

# Ensure the project root is importable when this file is run directly.
PROJECT_ROOT = cast(str, os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from Algorithms.Build.DefaultPlacement import defaultPlacement
from Algorithms.Build.InfluenceListGreedy import influenceListGreedy
from Algorithms.Build.RandomGreedy import randomGreedy
from Algorithms.Build.RandomPlacement import RandomPlacement
from Algorithms.Composite.Anealing import anealingFromRandom
from Algorithms.Composite.BruteForce import bruteForceFromRandom
from Algorithms.Composite.FluentWithSwitch import FluentWithSwitch
from Algorithms.Composite.RandomSwitch import randomSwitchFromRandom
from Algorithms.Composite.RepeatedRandom import repeatedRandom
from Algorithms.Composite.tabuSearch import tabuSearchFromRandom
from Utils.printer import printArrangementWithValues, printAsGraph
from Utils.reader import readPeople

from Utils import ValueCalc
from Utils.UtilFunctions import makeEmptyArrangement


ALGORITHMS = {
    "defaultPlacement": defaultPlacement,
    "influenceListGreedy": influenceListGreedy,
    "randomGreedy": randomGreedy,
    "randomPlacement": RandomPlacement,
    "repeatedRandom": repeatedRandom,
    "FluentWithSwitch": FluentWithSwitch,
    "anealing": anealingFromRandom,
    "bruteForce": bruteForceFromRandom,
    "randomSwitch": randomSwitchFromRandom,
    "tabuSearch": tabuSearchFromRandom,
    "createGraph": printAsGraph
    "repeatedSwitch": RepeatedLinearSwitch,
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) != 4:
        print("Usage: python runAlgorithm.py <algorithm> <input_file> <attribute_set_file>")
        print("\nAvailable algorithms:")
        for algo in ALGORITHMS:
            print(f"  - {algo}")
        print("\nExample:")
        print("  python runAlgorithm.py FluentWithSwitch Inputs/sheetOutput/Test\\ \\(svar\\)input.json Inputs/sheetOutput/Test\\ \\(svar\\)attribute_set.json")
        raise SystemExit(1)

    algorithm_name = sys.argv[1]
    input_file = sys.argv[2]
    attribute_set_file = sys.argv[3]

    # Validate algorithm
    if algorithm_name not in ALGORITHMS:
        print(f"Error: Unknown algorithm '{algorithm_name}'")
        print(f"Available algorithms: {', '.join(sorted(ALGORITHMS))}")
        raise SystemExit(1)

    # Load input and attribute set
    try:
        testInput = readPeople(input_file, attribute_set_file)
    except Exception as e:
        print(f"Error loading input: {e}")
        raise SystemExit(1)

    if not testInput or len(testInput) == 0:
        print(f"Error: Input is empty")
        raise SystemExit(1)

    print(f"Using algorithm: {algorithm_name}")
    print(f"Using input file: {input_file}")
    print(f"Using attribute set: {attribute_set_file}")
    print(f"Number of people: {len(testInput)}")
    print(f"Theory max: {ValueCalc.calcTheoreticalMax(testInput)}")
    print()

    # Create initial arrangement
    initial_arrangement = makeEmptyArrangement(len(testInput), 8)

    # Run the algorithm with the shared (input, emptyArrangement) signature
    result_arrangement = ALGORITHMS[algorithm_name](testInput, initial_arrangement)

    printArrangementWithValues(result_arrangement)

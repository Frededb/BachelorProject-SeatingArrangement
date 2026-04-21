import os
import sys
from typing import cast

# Ensure the project root is importable when this file is run directly.
PROJECT_ROOT = cast(str, os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


from Algorithms.Build.DefaultPlacement import defaultPlacement
from Algorithms.Build.InfluenceListGreedy import influenceListGreedy
from Algorithms.Build.RandomGreedy import randomGreedy
from Algorithms.Composite.AnealingFromFluent import annealingFromFluent
from Algorithms.Composite.AnealingFromRandom import annealingFromRandom
from Algorithms.Composite.BruteForce import bruteForceFromRandom
from Algorithms.Composite.LinearSwitchFromFluent import linearSwitchFromFluent
from Algorithms.Composite.LinearSwitchFromFluentProtected import linearSwitchFromFluentProtected
from Algorithms.Composite.LinearSwitchFromRandom import linearSwitchFromRandom
from Algorithms.Composite.RandomSwitchFromFluent import randomSwitchFromFluent
from Algorithms.Composite.RandomSwitchFromRandom import randomSwitchFromRandom
from Algorithms.Composite.RepeatedRandom import repeatedRandom
from Algorithms.Composite.TabuSearchFromFluent import tabuSearchFromFluent
from Algorithms.Composite.TabuSearchFromRandom import tabuSearchFromRandom
from Utils.printer import printArrangementWithValues, printAsGraph
from Utils.reader import readPeople

from Utils import ValueCalc
from Utils.UtilFunctions import makeEmptyArrangement


ALGORITHMS = {
    "defaultPlacement": defaultPlacement,
    "influenceListGreedy": influenceListGreedy,
    "randomGreedy": randomGreedy,
    "annealingFromFluent": annealingFromFluent,
    "annealingFromRandom": annealingFromRandom,
    "bruteForce": bruteForceFromRandom,
    "linearSwitchFromFluent": linearSwitchFromFluent,
    "linearSwitchFromFluentProtected": linearSwitchFromFluentProtected,
    "linearSwitchFromRandom": linearSwitchFromRandom,
    "randomSwitchFromFluent": randomSwitchFromFluent,
    "randomSwitchFromRandom": randomSwitchFromRandom,
    "repeatedRandom": repeatedRandom,
    "tabuSearchFromFluent": tabuSearchFromFluent,
    "tabuSearchFromRandom": tabuSearchFromRandom,
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) != 4:
        print("Usage: python runAlgorithm.py <algorithm> <input_file> <attribute_set_file>")
        print("\nAvailable algorithms:")
        for algo in ALGORITHMS:
            print(f"  - {algo}")
        print("\nExample:")
        print("  python runAlgorithm.py annealingFromFluent Inputs/sheetOutput/Test\\ \\(svar\\)input.json Inputs/sheetOutput/Test\\ \\(svar\\)attribute_set.json")
        raise SystemExit(1)

    algorithm_name = sys.argv[1]
    input_file = sys.argv[2]
    attribute_set_file = sys.argv[3]

    if algorithm_name == "printGraph":
        try:
            testInput = readPeople(input_file, attribute_set_file)
            printAsGraph(testInput)
        except Exception as e:
            print(f"Error loading input for graph: {e}")
            raise SystemExit(1)
        raise SystemExit(0)

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
    print()

    # Create initial arrangement
    initial_arrangement = makeEmptyArrangement(len(testInput), 8)

    # Run the algorithm with the shared (input, emptyArrangement) signature
    result_arrangement = ALGORITHMS[algorithm_name](testInput, initial_arrangement)

    printArrangementWithValues(result_arrangement)

import os
import sys
from pathlib import Path
from typing import Any, cast

# Ensure the project root is importable when this file is run directly.
PROJECT_ROOT = cast(str, os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


from Algorithms.Build.DefaultPlacement import defaultPlacement
from Algorithms.Build.FluentGroupsFill import fluentGroupsFill
from Algorithms.Build.InfluenceListGreedy import influenceListGreedy
from Algorithms.Build.RandomGreedy import randomGreedy
from Algorithms.Build.RandomPlacement import randomPlacement
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
from Algorithms.Disruption.TearDown import TearDown
from Algorithms.Optimizing.Anealing import annealing
from Algorithms.Optimizing.BruteForce import bruteForce
from Algorithms.Optimizing.LinearSwitchPeopleSets import LinearSwitchPeopleSets, linearSwitchPeopleEachTable
from Algorithms.Optimizing.RandomSwitch import randomSwitch
from Algorithms.Optimizing.RepeatedLinearSwitch import repeatedLinearSwitch
from Algorithms.Optimizing.Switch2PeopleRandom import Switch2PeopleRandom
from Algorithms.Optimizing.TabuSearch import tabuSearch
from Utils.printer import printArrangementWithValues, printAsGraph
from Utils.reader import readPeople

from Utils import ValueCalc
from Utils.UtilFunctions import makeEmptyArrangement, makeEmptyArrangementFromTableSizes


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


def _build_fluent_groups_fill(input_people, empty_arrangement):
    arrangement, _protected_names = fluentGroupsFill(input_people, empty_arrangement)
    return arrangement


def _linear_switch_each_table_v3(arrangement):
    return linearSwitchPeopleEachTable(arrangement, 3)


def _repeated_linear_switch_v3(arrangement):
    return repeatedLinearSwitch(arrangement, 3)



BUILD_ALGORITHMS = {
    "defaultPlacement": defaultPlacement,
    "influenceListGreedy": influenceListGreedy,
    "randomGreedy": randomGreedy,
    "randomPlacement": randomPlacement,
    "fluentGroupsFill": _build_fluent_groups_fill,
}

OPTIMIZING_ALGORITHMS = {
    "annealing": annealing,
    "bruteForce": bruteForce,
    "linearSwitchPeopleEachTable(v=3)": _linear_switch_each_table_v3,
    "randomSwitch": randomSwitch,
    "repeatedLinearSwitch(v=3)": _repeated_linear_switch_v3,
    "switch2PeopleRandom": Switch2PeopleRandom,
    "tabuSearch": tabuSearch,
}

DISRUPTION_ALGORITHMS = {
    "tearDown": TearDown,
}

PIPELINE_ALGORITHMS = {
    **OPTIMIZING_ALGORITHMS,
    **DISRUPTION_ALGORITHMS,
}

PIPELINE_ALGORITHMS_BY_GROUP = {
    "build": BUILD_ALGORITHMS,
    "optimizing": OPTIMIZING_ALGORITHMS,
    "disruption": DISRUPTION_ALGORITHMS,
}


def _build_initial_arrangement(test_input: list[Any], table_sizes: list[int] | None, default_table_size: int) -> list[list[Any]]:
    if table_sizes:
        initial_arrangement = makeEmptyArrangementFromTableSizes(table_sizes)
    else:
        initial_arrangement = makeEmptyArrangement(len(test_input), default_table_size)

    total_capacity = sum(len(table) for table in initial_arrangement)
    if total_capacity < len(test_input):
        raise ValueError(
            f"Not enough seats in empty arrangement: capacity {total_capacity}, people {len(test_input)}"
        )
    return initial_arrangement


def _score_result(algorithm_name: str, arrangement: list[list[Any]], test_input: list[Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    total_value, table_values, people_values = ValueCalc.calcArrangement(arrangement)
    result: dict[str, Any] = {
        "algorithm": algorithm_name,
        "people_count": len(test_input),
        "arrangement": arrangement,
        "total_value": total_value,
        "table_values": table_values,
        "people_values": people_values,
    }
    if extra:
        result.update(extra)
    return result


def run_composite_pipeline(
    build_algorithm_name: str,
    stage_names: list[str],
    input_file: str | Path | dict[str, Any],
    attribute_set_file: str | Path | dict[str, Any],
    table_sizes: list[int] | None = None,
    default_table_size: int = 8,
) -> dict[str, Any]:
    if build_algorithm_name not in BUILD_ALGORITHMS:
        raise ValueError(
            f"Unknown build algorithm '{build_algorithm_name}'. Available build algorithms: {', '.join(sorted(BUILD_ALGORITHMS))}"
        )

    unknown_stages = [name for name in stage_names if name not in PIPELINE_ALGORITHMS]
    if unknown_stages:
        raise ValueError(
            f"Unknown pipeline stage(s): {', '.join(unknown_stages)}. Available stages: {', '.join(sorted(PIPELINE_ALGORITHMS))}"
        )

    test_input = readPeople(input_file, attribute_set_file)
    if not test_input:
        raise ValueError("Input is empty")

    initial_arrangement = _build_initial_arrangement(test_input, table_sizes, default_table_size)
    arrangement = BUILD_ALGORITHMS[build_algorithm_name](test_input, initial_arrangement)

    for stage_name in stage_names:
        arrangement = PIPELINE_ALGORITHMS[stage_name](arrangement)

    pipeline_label = " -> ".join([build_algorithm_name, *stage_names]) if stage_names else build_algorithm_name
    return _score_result(
        pipeline_label,
        arrangement,
        test_input,
        extra={
            "build_algorithm": build_algorithm_name,
            "stages": list(stage_names),
        },
    )


def run_selected_algorithm(
    algorithm_name: str,
    input_file: str | Path | dict[str, Any],
    attribute_set_file: str | Path | dict[str, Any],
    table_sizes: list[int] | None = None,
    default_table_size: int = 8,
) -> dict[str, Any]:
    if algorithm_name not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm '{algorithm_name}'. Available algorithms: {', '.join(sorted(ALGORITHMS))}")

    test_input = readPeople(input_file, attribute_set_file)
    if not test_input:
        raise ValueError("Input is empty")

    initial_arrangement = _build_initial_arrangement(test_input, table_sizes, default_table_size)

    result_arrangement = ALGORITHMS[algorithm_name](test_input, initial_arrangement)
    return _score_result(algorithm_name, result_arrangement, test_input)


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

    print(f"Using algorithm: {algorithm_name}")
    print(f"Using input file: {input_file}")
    print(f"Using attribute set: {attribute_set_file}")

    try:
        result = run_selected_algorithm(algorithm_name, input_file, attribute_set_file)
    except Exception as e:
        print(f"Error running algorithm: {e}")
        raise SystemExit(1)

    print(f"Number of people: {result['people_count']}")
    print()
    printArrangementWithValues(result["arrangement"])

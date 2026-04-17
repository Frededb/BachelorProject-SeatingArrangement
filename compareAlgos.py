import json
import statistics
import time
import copy
from generatData import generateData
from Utils.Person import Person
from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import makeEmptyArrangement
from Utils.reader import readPeople
import os

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
from Algorithms.Composite.RepeatedLinearSwitch import RepeatedLinearSwitch

    # "randomPlacement": RandomPlacement,
    # "godscore"
ALGORITHMS = {
    "influenceListGreedy": influenceListGreedy,
    "randomGreedy": randomGreedy,
    "bruteForce": bruteForceFromRandom,
    "anealing": anealingFromRandom,
    "tabuSearch": tabuSearchFromRandom,
    "repeatedSwitch": RepeatedLinearSwitch,
}

def compare_algos():
    attribute_set = [
        {"index": 0, "header": "studyprogram", "kind": "traits", "weight": 3},
        {"index": 1, "header": "year", "kind": "traits", "weight": 1},
        {"index": 2, "header": "preferences", "kind": "prefence", "weight": 15},
        {"index": 3, "header": "avoidances", "kind": "prefence", "weight": -30}
    ]
    
    cohesion_scores = [20, 50, 80]# [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    iterations = 2
    people_count = 10
    
    # Initialize results
    results = {algo: {c: [] for c in cohesion_scores} for algo in ALGORITHMS}
    time_results = {algo: {c: [] for c in cohesion_scores} for algo in ALGORITHMS}
    
    # Create an output path for the temporary generated data or let generateData dump to a tmp file
    temp_output_file = "Inputs/temp/compareGenerated.json"
    attribute_set_file = "Inputs/defaultAttributeSet.json"
    
    for algo_name, algo_func in ALGORITHMS.items():
        print(f"Running iterations for algorithm: {algo_name}")
        # if algo_name == "bruteForce" or algo_name == "switch4People":
        #     print("  Skipping due to expected long runtime")
            # continue
        for c in cohesion_scores:
            for i in range(iterations):
                generateData(people_count, c, temp_output_file, seed=i*157)
            
                # Always read fresh Person objects for each algorithm to avoid mutation
                try:
                    testInput = readPeople(temp_output_file, attribute_set_file)
                    initial_arrangement = makeEmptyArrangement(len(testInput), 8)
                
                    start_time = time.time()
                    result_arrangement = algo_func(testInput, initial_arrangement)
                    end_time = time.time()
                    
                    totalValue, _, _ = calcArrangement(result_arrangement)
                    results[algo_name][c].append(totalValue)
                    time_results[algo_name][c].append(end_time - start_time)
                except Exception as e:
                    print(f"  Error in {algo_name} at cohesion {c}, iter {i}: {e}")
                    results[algo_name][c].append(0)
                    time_results[algo_name][c].append(0)
                    
    # Clean up temp file
    if os.path.exists(temp_output_file):
        os.remove(temp_output_file)

    print("\n" + "="*80)
    print("AVERAGE ARRANGEMENT SCORES")
    print("="*80)
    
    # Header
    print(f"{'Algorithm':<25}", end="")
    for c in cohesion_scores:
        print(f"{c:>7}", end="")
    print("\n" + "-"*80)
    
    for algo_name in ALGORITHMS:
        print(f"{algo_name:<25}", end="")
        for c in cohesion_scores:
            scores = results[algo_name][c]
            avg = sum(scores) / len(scores) if scores else 0
            print(f"{avg:>6.1f} ", end="")
        print()

    print("\n" + "="*80)
    print("AVERAGE EXECUTION TIMES (seconds)")
    print("="*80)
    
    # Header
    print(f"{'Algorithm':<25}", end="")
    for c in cohesion_scores:
        print(f"{c:>7}", end="")
    print("\n" + "-"*80)
    
    for algo_name in ALGORITHMS:
        print(f"{algo_name:<25}", end="")
        for c in cohesion_scores:
            times = time_results[algo_name][c]
            avg_time = sum(times) / len(times) if times else 0
            print(f"{avg_time:>6.4f} ", end="")
        print()

if __name__ == "__main__":
    compare_algos()

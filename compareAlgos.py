import json
import statistics
import copy
from generatData import generateData
from runAlgorithm import ALGORITHMS
from Utils.Person import Person
from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import makeEmptyArrangement
from Utils.reader import readPeople
import os

def compare_algos():
    attribute_set = [
        {"index": 0, "header": "studyprogram", "kind": "traits", "weight": 3},
        {"index": 1, "header": "year", "kind": "traits", "weight": 1},
        {"index": 2, "header": "preferences", "kind": "prefence", "weight": 15},
        {"index": 3, "header": "avoidances", "kind": "prefence", "weight": -30}
    ]
    
    cohesion_scores = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    iterations = 10
    people_count = 100
    
    # Initialize results
    results = {algo: {c: [] for c in cohesion_scores} for algo in ALGORITHMS}
    
    # Create an output path for the temporary generated data or let generateData dump to a tmp file
    temp_output_file = "Inputs/temp/compareGenerated.json"
    attribute_set_file = "Inputs/defaultAttributeSet.json"
    
    for algo_name, algo_func in ALGORITHMS.items():
        print(f"Running iterations for algorithm: {algo_name}")
        for c in cohesion_scores:
            for i in range(iterations):
                generateData(people_count, c, temp_output_file, seed=i*157)
            
                # Always read fresh Person objects for each algorithm to avoid mutation
                try:
                    testInput = readPeople(temp_output_file, attribute_set_file)
                    initial_arrangement = makeEmptyArrangement(len(testInput), 8)
                
                    result_arrangement = algo_func(testInput, initial_arrangement)
                    totalValue, _, _ = calcArrangement(result_arrangement)
                    results[algo_name][c].append(totalValue)
                except Exception as e:
                    print(f"  Error in {algo_name} at cohesion {c}, iter {i}: {e}")
                    results[algo_name][c].append(0)
                    
    # Clean up temp file
    if os.path.exists(temp_output_file):
        os.remove(temp_output_file)

    print("\n" + "="*80)
    print("AVERAGE ARRANGEMENT SCORES")
    print("="*80)
    
    # Header
    print(f"{'Algorithm':<25}", end="")
    for c in cohesion_scores:
        print(f"{c:>6}", end="")
    print("\n" + "-"*80)
    
    for algo_name in ALGORITHMS:
        print(f"{algo_name:<25}", end="")
        for c in cohesion_scores:
            scores = results[algo_name][c]
            avg = sum(scores) / len(scores) if scores else 0
            print(f"{avg:>6.1f}", end="")
        print()

if __name__ == "__main__":
    compare_algos()

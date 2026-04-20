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
import tempfile
import multiprocessing

os.environ["TMPDIR"] = "/tmp"
tempfile.tempdir = "/tmp"

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

def run_algo_wrapper(algo_func, testInput, initial_arrangement, return_dict):
    try:
        result = algo_func(testInput, initial_arrangement)
        totalValue, _, _ = calcArrangement(result)
        return_dict['value'] = totalValue
        return_dict['success'] = True
    except Exception as e:
        return_dict['error'] = str(e)
        return_dict['success'] = False

def compare_algos():
    attribute_set = [
        {"index": 0, "header": "studyprogram", "kind": "traits", "weight": 3},
        {"index": 1, "header": "year", "kind": "traits", "weight": 1},
        {"index": 2, "header": "preferences", "kind": "prefence", "weight": 15},
        {"index": 3, "header": "avoidances", "kind": "prefence", "weight": -30}
    ]
    
    cohesion_scores = [20, 50, 80]# [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    iterations = 10
    people_counts = [8, 30, 100]
    
    # Initialize results
    results = {algo: {p: {c: [] for c in cohesion_scores} for p in people_counts} for algo in ALGORITHMS}
    time_results = {algo: {p: {c: [] for c in cohesion_scores} for p in people_counts} for algo in ALGORITHMS}
    
    # Create an output path for the temporary generated data in /tmp to avoid read-only FS in container
    temp_output_file = "/tmp/compareGenerated.json"
    attribute_set_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Inputs", "defaultAttributeSet.json")
    
    for algo_name, algo_func in ALGORITHMS.items():
        print(f"Running iterations for algorithm: {algo_name}")
        # if algo_name == "bruteForce" or algo_name == "switch4People":
        #     print("  Skipping due to expected long runtime")
            # continue
        for p_count in people_counts:
            for c in cohesion_scores:
                timeouts_limit = 3
                for i in range(iterations):
                    generateData(p_count, c, temp_output_file, seed=i*157)
                
                    # Always read fresh Person objects for each algorithm to avoid mutation
                    try:
                        testInput = readPeople(temp_output_file, attribute_set_file)
                        initial_arrangement = makeEmptyArrangement(len(testInput), 8)
                    
                        with multiprocessing.Manager() as manager:
                            return_dict = manager.dict()
                            return_dict['success'] = False
                            
                            start_time = time.time()
                            p = multiprocessing.Process(target=run_algo_wrapper, args=(algo_func, testInput, initial_arrangement, return_dict))
                            p.start()
                            limit = 30
                            p.join(limit) # timeout
                            
                            if p.is_alive():
                                print(f"  Timeout! {algo_name} at size {p_count}, cohesion {c}, iter {i} took longer than {limit} seconds.")
                                p.terminate()
                                p.join()
                                results[algo_name][p_count][c].append("DNF")
                                time_results[algo_name][p_count][c].append("DNF")
                                
                                timeouts_limit -= 1
                                if timeouts_limit == 0:
                                    print(f"  First 3 runs timed out. Cancelling remaining iterations.")
                                    remaining = iterations - (i + 1)
                                    results[algo_name][p_count][c].extend(["DNF"] * remaining)
                                    time_results[algo_name][p_count][c].extend(["DNF"] * remaining)
                                    break
                                
                                continue
                                
                            timeouts_limit = -1
                            end_time = time.time()
                            
                            if return_dict.get('success'):
                                totalValue = return_dict['value']
                                results[algo_name][p_count][c].append(totalValue)
                                time_results[algo_name][p_count][c].append(end_time - start_time)
                            else:
                                error_msg = return_dict.get('error', 'Unknown Error')
                                print(f"  Error in {algo_name} at cohesion {c}, iter {i}: {error_msg}")
                                results[algo_name][p_count][c].append("DNF")
                                time_results[algo_name][p_count][c].append("DNF")
                            
                    except Exception as e:
                        print(f"  Error setting up {algo_name} at cohesion {c}, iter {i}: {e}")
                        results[algo_name][p_count][c].append("DNF")
                        time_results[algo_name][p_count][c].append("DNF")
                print(f"  Completed {iterations} iterations for size {p_count}, cohesion {c}.")
                    
    # Clean up temp file
    if os.path.exists(temp_output_file):
        os.remove(temp_output_file)

    print("\n" + "="*80)
    for p_count in people_counts:
        print(f"AVERAGE ARRANGEMENT SCORES (People: {p_count})")
        print("="*80)
        
        # Header
        print(f"{'Algorithm':<25}", end="")
        for c in cohesion_scores:
            print(f"{c:>7}", end="")
        print("\n" + "-"*80)
        
        for algo_name in ALGORITHMS:
            print(f"{algo_name:<25}", end="")
            for c in cohesion_scores:
                scores = [s for s in results[algo_name][p_count][c] if s != "DNF"]
                avg = sum(scores) / len(scores) if scores else "DNF"
                if avg == "DNF":
                    print(f"{'DNF':>6} ", end="")
                else:
                    print(f"{avg:>6.1f} ", end="")
            print()
        print("\n" + "="*80)

    for p_count in people_counts:
        print(f"AVERAGE EXECUTION TIMES (seconds) (People: {p_count})")
        print("="*80)
        
        # Header
        print(f"{'Algorithm':<25}", end="")
        for c in cohesion_scores:
            print(f"{c:>7}", end="")
        print("\n" + "-"*80)
        
        for algo_name in ALGORITHMS:
            print(f"{algo_name:<25}", end="")
            for c in cohesion_scores:
                times = [t for t in time_results[algo_name][p_count][c] if t != "DNF"]
                avg_time = sum(times) / len(times) if times else "DNF"
                if avg_time == "DNF":
                    print(f"{'DNF':>6} ", end="")
                else:
                    print(f"{avg_time:>6.4f} ", end="")
            print()
        print("\n" + "="*80)

    # Helper function for JSON export safely handling DNF
    def get_avg(data_list):
        valid = [x for x in data_list if x != "DNF"]
        return sum(valid) / len(valid) if valid else "DNF"

    # Write results to JSON file
    output_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M"),
        "cohesion_scores": cohesion_scores,
        "iterations": iterations,
        "people_counts": people_counts,
        "results": {
            algo: {
                str(p): {
                    str(c): {
                        "scores": results[algo][p][c],
                        "times": time_results[algo][p][c],
                        "avg_score": get_avg(results[algo][p][c]),
                        "avg_time": get_avg(time_results[algo][p][c])
                    } for c in cohesion_scores
                } for p in people_counts
            } for algo in ALGORITHMS
        }
    }
    
    timestamp_file = time.strftime("%y%m%d_%H%M")
    filename = f"comparison_results_{timestamp_file}.json"
    
    with open(filename, "w") as f:
        json.dump(output_data, f, indent=4)
    print(f"\nResults successfully written to {filename}")

if __name__ == "__main__":
    compare_algos()

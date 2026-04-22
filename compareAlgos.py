import argparse
import json
import time
from generateData import generateData
from Utils.ValueCalc import calcArrangement
from Utils.UtilFunctions import makeEmptyArrangement
from Utils.reader import parsePeople
import os
import tempfile
import multiprocessing
import gc

os.environ["TMPDIR"] = "/tmp"
tempfile.tempdir = "/tmp"

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
from Algorithms.Legacy.RepeatedRandom import repeatedRandom
from Algorithms.Composite.TabuSearchFromFluent import tabuSearchFromFluent
from Algorithms.Composite.TabuSearchFromRandom import tabuSearchFromRandom

    # "randomPlacement": RandomPlacement,
    # "godscore"
ALGORITHMS = {
    "defaultPlacement": defaultPlacement,
    "influenceListGreedy": influenceListGreedy,
    "randomGreedy": randomGreedy,
    "annealingFromFluent": annealingFromFluent,
    "annealingFromRandom": annealingFromRandom,
    "linearSwitchFromFluent": linearSwitchFromFluent,
    "linearSwitchFromFluentProtected": linearSwitchFromFluentProtected,
    "linearSwitchFromRandom": linearSwitchFromRandom,
    "randomSwitchFromFluent": randomSwitchFromFluent,
    "randomSwitchFromRandom": randomSwitchFromRandom,
    "repeatedRandom": repeatedRandom,
    "tabuSearchFromFluent": tabuSearchFromFluent,
    "tabuSearchFromRandom": tabuSearchFromRandom,
    "bruteForce": bruteForceFromRandom,
}

cohesion_scores = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
iterations = 100
people_counts = [8, 30, 100, 300]


def print_results(results, time_results, cohesion_scores, people_counts, quicksave=False, algo_filter=None):
    # Helper function for JSON export safely handling DNF
    def get_avg(data_list):
        valid = [x for x in data_list if x != "DNF"]
        return sum(valid) / len(valid) if valid else "DNF"

    # Write results to JSON file
    output_data = {
        "full_dataset": not quicksave,
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
            } for algo in results
        }
    }
    
    timestamp_file = time.strftime("%y%m%d_%H%M")
    algo_suffix = f"_{algo_filter}" if algo_filter else ""
    filename = f"comparison_results{algo_suffix}_{timestamp_file}.json"
    
    with open(filename, "w") as f:
        json.dump(output_data, f, indent=4)
    print(f"\nResults successfully written to {filename}")

def run_algo_wrapper(algo_func, testInput, initial_arrangement, send_conn):
    try:
        result = algo_func(testInput, initial_arrangement)
        totalValue, _, _ = calcArrangement(result)
        send_conn.send({'success': True, 'value': totalValue})
    except Exception as e:
        send_conn.send({'success': False, 'error': str(e)})
    finally:
        try:
            send_conn.close()
        except Exception:
            pass

def compare_algos(algo_filter=None):
    attribute_set = [
        {"index": 0, "header": "studyprogram", "kind": "traits", "weight": 3},
        {"index": 1, "header": "year", "kind": "traits", "weight": 1},
        {"index": 2, "header": "preferences", "kind": "prefence", "weight": 15},
        {"index": 3, "header": "avoidances", "kind": "prefence", "weight": -30}
    ]
    
    run_algos = {k: v for k, v in ALGORITHMS.items() if algo_filter is None or k == algo_filter}
    if not run_algos:
        print(f"Error: Algorithm '{algo_filter}' not found. Available: {list(ALGORITHMS.keys())}")
        return

    # Initialize results
    results = {algo: {p: {c: [] for c in cohesion_scores} for p in people_counts} for algo in run_algos}
    time_results = {algo: {p: {c: [] for c in cohesion_scores} for p in people_counts} for algo in run_algos}
    
    attribute_set_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Inputs", "defaultAttributeSet.json")
    with open(attribute_set_file, encoding="utf-8") as f:
        attribute_set_data = json.load(f)
    attribute_set = attribute_set_data.get("attribute_set", []) if isinstance(attribute_set_data, dict) else []
    
    for algo_name, algo_func in run_algos.items():
        print(f"Running iterations for algorithm: {algo_name}")
        # if algo_name == "bruteForce" or algo_name == "switch4People":
        #     print("  Skipping due to expected long runtime")
            # continue
        for p_count in people_counts:
            for c in cohesion_scores:
                timeouts_limit = 10
                for i in range(iterations):
                    people_data = generateData(p_count, c, seed=i*157)
                
                    # Always read fresh Person objects for each algorithm to avoid mutation
                    try:
                        p = None
                        recv_conn = None
                        send_conn = None
                        
                        testInput = parsePeople({"people": people_data}, attribute_set)
                        initial_arrangement = makeEmptyArrangement(len(testInput), 8)
                    
                        recv_conn, send_conn = multiprocessing.Pipe(duplex=False)
                        
                        start_time = time.time()
                        p = multiprocessing.Process(target=run_algo_wrapper, args=(algo_func, testInput, initial_arrangement, send_conn))
                        p.start()
                        
                        # Close the write end in the parent process so it doesn't hang
                        send_conn.close()
                        send_conn = None
                        
                        limit = 30
                        p.join(limit) # timeout
                        
                        if p.is_alive():
                            print(f"  Timeout! {algo_name} at size {p_count}, cohesion {c}, iter {i} took longer than {limit} seconds.")
                            p.terminate()
                            p.join()
                            p.close()
                            if recv_conn:
                                recv_conn.close()
                                recv_conn = None
                            results[algo_name][p_count][c].append("DNF")
                            time_results[algo_name][p_count][c].append("DNF")
                            
                            timeouts_limit -= 1
                            if timeouts_limit == 0:
                                print(f"  First 10 runs timed out. Cancelling remaining iterations.")
                                remaining = iterations - (i + 1)
                                results[algo_name][p_count][c].extend(["DNF"] * remaining)
                                time_results[algo_name][p_count][c].extend(["DNF"] * remaining)
                                break
                            
                            continue
                            
                        timeouts_limit = -1
                        end_time = time.time()
                        
                        return_dict = {'success': False, 'error': f'Process crashed or returned no output, exitcode: {p.exitcode}'}
                        if p.exitcode == 0:
                            if recv_conn.poll(0.1):  # Wait up to 0.1s to read success state from the pipe
                                try:
                                    return_dict = recv_conn.recv()
                                except EOFError:
                                    pass
                        
                        recv_conn.close()
                        recv_conn = None
                        p.close()
                        
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
                    finally:
                        for obj in [send_conn, recv_conn]:
                            try:
                                if obj:
                                    obj.close()
                            except Exception:
                                pass
                        try:
                            if p:
                                p.close()
                        except Exception:
                            pass
                        gc.collect()
                print(f"  Completed {iterations} iterations for size {p_count}, cohesion {c}.")
        print_results(results, time_results, cohesion_scores, people_counts, quicksave=True, algo_filter=algo_filter)
                    
    print("\n" + "="*80)
    for p_count in people_counts:
        print(f"AVERAGE ARRANGEMENT SCORES (People: {p_count})")
        print("="*80)
        
        # Header
        print(f"{'Algorithm':<25}", end="")
        for c in cohesion_scores:
            print(f"{c:>7}", end="")
        print("\n" + "-"*80)
        
        for algo_name in run_algos:
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
        
        for algo_name in run_algos:
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

    print_results(results, time_results, cohesion_scores, people_counts, algo_filter=algo_filter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare seating algorithms")
    parser.add_argument("--algo", default=None, help="Run only this algorithm (default: run all)")
    args = parser.parse_args()
    compare_algos(algo_filter=args.algo)

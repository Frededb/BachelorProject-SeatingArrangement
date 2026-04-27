import argparse
import json
import time
from generateData import generateData
from Utils.ValueCalc import calcArrangement, calcTheoreticalMax
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

ALGORITHMS = {
    # "defaultPlacement": defaultPlacement,
    # "influenceListGreedy": influenceListGreedy,
    # "randomGreedy": randomGreedy,
    "annealingFromFluent": annealingFromFluent,
    "annealingFromRandom": annealingFromRandom,
    "linearSwitchFromFluent": linearSwitchFromFluent,
    "linearSwitchFromFluentProtected": linearSwitchFromFluentProtected,
    "linearSwitchFromRandom": linearSwitchFromRandom,
    "randomSwitchFromFluent": randomSwitchFromFluent,
    "randomSwitchFromRandom": randomSwitchFromRandom,
    "tabuSearchFromFluent": tabuSearchFromFluent,
    "tabuSearchFromRandom": tabuSearchFromRandom,
    "bruteForce": bruteForceFromRandom,
    "theoreticalMax": lambda testInput, initial_arrangement, timelimit: calcTheoreticalMax(testInput, initial_arrangement),
}

cohesion_scores = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
iterations = 100
people_counts = [100] #8, 30, 100, 
timelimits = [60]


def print_results(results, time_results, cohesion_scores, people_counts, quicksave=False, algo_filter=None, output_dir=None):
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
        "timelimits": timelimits,
        "results": {
            algo: {
                str(tl): {
                    str(p): {
                        str(c): {
                            "scores": results[algo][tl][p][c],
                            "times": time_results[algo][tl][p][c],
                            "avg_score": get_avg(results[algo][tl][p][c]),
                            "avg_time": get_avg(time_results[algo][tl][p][c])
                        } for c in cohesion_scores
                    } for p in people_counts
                } for tl in timelimits
            } for algo in results
        }
    }
    
    algo_suffix = f"_{algo_filter}" if algo_filter else ""
    filename = f"comparison_results{algo_suffix}.json"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)

    with open(filename, "w") as f:
        json.dump(output_data, f, indent=4)
    print(f"\nResults successfully written to {filename}")

def run_algo_wrapper(algo_func, testInput, initial_arrangement, send_conn, timelimit):
    try:
        result = algo_func(testInput, initial_arrangement, timelimit)
        if isinstance(result, (int, float)):
            totalValue = result
        else:
            totalValue, _, _ = calcArrangement(result)
        send_conn.send({'success': True, 'value': totalValue})
    except Exception as e:
        send_conn.send({'success': False, 'error': str(e)})
    finally:
        try:
            send_conn.close()
        except Exception:
            pass

def compare_algos(algo_filter=None, output_dir=None):
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
    results = {algo: {tl: {p: {c: [] for c in cohesion_scores} for p in people_counts} for tl in timelimits} for algo in run_algos}
    time_results = {algo: {tl: {p: {c: [] for c in cohesion_scores} for p in people_counts} for tl in timelimits} for algo in run_algos}
    
    attribute_set_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Inputs", "defaultAttributeSet.json")
    with open(attribute_set_file, encoding="utf-8") as f:
        attribute_set_data = json.load(f)
    attribute_set = attribute_set_data.get("attribute_set", []) if isinstance(attribute_set_data, dict) else []
    
    for algo_name, algo_func in run_algos.items():
        print(f"Running iterations for algorithm: {algo_name}")
        # if algo_name == "bruteForce" or algo_name == "switch4People":
        #     print("  Skipping due to expected long runtime")
            # continue
        for timelimit in timelimits:
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
                            p = multiprocessing.Process(target=run_algo_wrapper, args=(algo_func, testInput, initial_arrangement, send_conn, timelimit))
                            p.start()
                            
                            # Close the write end in the parent process so it doesn't hang
                            send_conn.close()
                            send_conn = None
                            
                            p.join(timelimit + 20)
                            
                            if p.is_alive():
                                print(f"  Timeout! {algo_name} at size {p_count}, cohesion {c}, iter {i} took longer than {timelimit} seconds.")
                                p.terminate()
                                p.join()
                                p.close()
                                if recv_conn:
                                    recv_conn.close()
                                    recv_conn = None
                                results[algo_name][timelimit][p_count][c].append("DNF")
                                time_results[algo_name][timelimit][p_count][c].append("DNF")
                                
                                timeouts_limit -= 1
                                if timeouts_limit == 0:
                                    print(f"  First 10 runs timed out. Cancelling remaining iterations.")
                                    remaining = iterations - (i + 1)
                                    results[algo_name][timelimit][p_count][c].extend(["DNF"] * remaining)
                                    time_results[algo_name][timelimit][p_count][c].extend(["DNF"] * remaining)
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
                                results[algo_name][timelimit][p_count][c].append(totalValue)
                                time_results[algo_name][timelimit][p_count][c].append(end_time - start_time)
                            else:
                                error_msg = return_dict.get('error', 'Unknown Error')
                                print(f"  Error in {algo_name} at cohesion {c}, iter {i}: {error_msg}")
                                results[algo_name][timelimit][p_count][c].append("DNF")
                                time_results[algo_name][timelimit][p_count][c].append("DNF")
                                
                        except Exception as e:
                            print(f"  Error setting up {algo_name} at cohesion {c}, iter {i}: {e}")
                            results[algo_name][timelimit][p_count][c].append("DNF")
                            time_results[algo_name][timelimit][p_count][c].append("DNF")
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
                    print(f"  Completed {iterations} iterations for size {p_count}, cohesion {c}, timelimit {timelimit}.")
            print_results(results, time_results, cohesion_scores, people_counts, quicksave=True, algo_filter=algo_filter, output_dir=output_dir)

    def avg_or_dnf(values):
        valid = [v for v in values if v != "DNF"]
        return sum(valid) / len(valid) if valid else "DNF"

    def fmt(v, fmt_str):
        return "DNF" if v == "DNF" else format(v, fmt_str)

    print("\n" + "="*80)
    print(f"{'Algorithm':<25} {'Timelimit':>10} {'People':>8} {'Avg Score':>12} {'Avg Time(s)':>12}")
    print("-"*80)
    for algo_name in run_algos:
        for tl in timelimits:
            for p_count in people_counts:
                all_scores = [s for c in cohesion_scores for s in results[algo_name][tl][p_count][c]]
                all_times = [t for c in cohesion_scores for t in time_results[algo_name][tl][p_count][c]]
                avg_score = avg_or_dnf(all_scores)
                avg_time = avg_or_dnf(all_times)
                print(f"{algo_name:<25} {tl:>10} {p_count:>8} {fmt(avg_score, '12.1f')} {fmt(avg_time, '12.4f')}")
    print("="*80)

    print_results(results, time_results, cohesion_scores, people_counts, algo_filter=algo_filter, output_dir=output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare seating algorithms")
    parser.add_argument("--algo", default=None, help="Run only this algorithm (default: run all)")
    parser.add_argument("--output", default=None, help="Directory to write output JSON files into")
    args = parser.parse_args()
    compare_algos(algo_filter=args.algo, output_dir=args.output)

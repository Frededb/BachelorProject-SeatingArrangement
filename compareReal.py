"""
Run all algorithms on the real input dataset and show a bar chart of scores.

Usage:
    python compareReal.py [--timelimit SECONDS]
"""

import argparse
import json
import os
import time
import multiprocessing
import threading

import matplotlib.pyplot as plt

from Utils.reader import readPeople
from Utils.UtilFunctions import makeEmptyArrangement
from Utils.ValueCalc import calcArrangement

from Algorithms.Composite.AnealingFromGrouped import annealingFromGrouped
from Algorithms.Composite.AnealingFromRandom import annealingFromRandom
from Algorithms.Composite.LinearSwitchFromGrouped import linearSwitchFromGrouped
from Algorithms.Composite.LinearSwitchFromGroupedProtected import linearSwitchFromGroupedProtected
from Algorithms.Composite.LinearSwitchFromRandom import linearSwitchFromRandom
from Algorithms.Composite.RandomSwitchFromGrouped import randomSwitchFromGrouped
from Algorithms.Composite.RandomSwitchFromRandom import randomSwitchFromRandom
from Algorithms.Composite.TabuSearchFromGrouped import tabuSearchFromGrouped
from Algorithms.Composite.TabuSearchFromRandom import tabuSearchFromRandom

ALGORITHMS = {
    "annealingFromGrouped":             annealingFromGrouped,
    "annealingFromRandom":             annealingFromRandom,
    "linearSwitchFromGrouped":          linearSwitchFromGrouped,
    "linearSwitchFromGroupedProtected": linearSwitchFromGroupedProtected,
    "linearSwitchFromRandom":          linearSwitchFromRandom,
    "randomSwitchFromGrouped":          randomSwitchFromGrouped,
    "randomSwitchFromRandom":          randomSwitchFromRandom,
    "tabuSearchFromGrouped":            tabuSearchFromGrouped,
    "tabuSearchFromRandom":            tabuSearchFromRandom,
}

INPUT_FILE = "Inputs/realData/inputReal.json"
ATTRIBUTE_SET_FILE = "Inputs/defaultAttributeSet.json"


def run_algo_worker(algo_func, testInput, initial_arrangement, send_conn, timelimit):
    score_tracker = [0.0]
    done_event = threading.Event()

    def reporter():
        while not done_event.wait(1.0):
            pass  # no timeline needed here

    try:
        result = algo_func(testInput, initial_arrangement, timelimit, score_tracker=score_tracker)
        if isinstance(result, (int, float)):
            score = result
        else:
            score, _, _ = calcArrangement(result)
        send_conn.send({"success": True, "score": score})
    except Exception as e:
        send_conn.send({"success": False, "error": str(e)})
    finally:
        done_event.set()
        try:
            send_conn.close()
        except Exception:
            pass


def run_algorithm(algo_name, algo_func, testInput, timelimit):
    initial_arrangement = makeEmptyArrangement(len(testInput), 8)
    recv_conn, send_conn = multiprocessing.Pipe(duplex=False)
    p = multiprocessing.Process(
        target=run_algo_worker,
        args=(algo_func, testInput, initial_arrangement, send_conn, timelimit)
    )
    p.start()
    send_conn.close()

    if recv_conn.poll(timelimit + 10):
        result = recv_conn.recv()
    else:
        result = {"success": False, "error": "timeout"}

    p.terminate()
    p.join()
    recv_conn.close()

    if result.get("success"):
        return result["score"]
    else:
        print(f"  [{algo_name}] failed: {result.get('error')}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timelimit", type=float, default=60.0)
    args = parser.parse_args()

    print(f"Loading {INPUT_FILE} ...")
    testInput = readPeople(INPUT_FILE, ATTRIBUTE_SET_FILE)
    print(f"  {len(testInput)} people loaded.")

    scores = {}
    for name, func in ALGORITHMS.items():
        print(f"Running {name} ...")
        start = time.perf_counter()
        score = run_algorithm(name, func, testInput, args.timelimit)
        elapsed = time.perf_counter() - start
        if score is not None:
            scores[name] = score
            print(f"  score={score:.2f}  time={elapsed:.1f}s")

    if not scores:
        print("No results to plot.")
        return

    # Bar chart
    names = list(scores.keys())
    values = [scores[n] for n in names]
    short_names = [n.replace("FromGrouped", "\n(Grouped)").replace("FromRandom", "\n(Random)") for n in names]

    fig, ax = plt.subplots()
    bars = ax.bar(short_names, values)
    ax.set_ylabel("Score")
    ax.set_title(f"Algorithm comparison on real data (timelimit={args.timelimit}s)")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    plt.tight_layout()
    plt.savefig("real_data_comparison.png", dpi=300, bbox_inches="tight")
    print("Saved to real_data_comparison.png")
    plt.show()


if __name__ == "__main__":
    main()

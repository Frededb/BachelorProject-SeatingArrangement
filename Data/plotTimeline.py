"""
Plot score-over-time for the first iteration of each algorithm at a given cohesion,
from a folder where each file contains one algorithm's data.

Usage:
    python plotTimeline.py [folder] [--people N] [--cohesion C] [--out FILE]

Defaults:
    folder    = jsonDataFullRun
    --people  = 300
    --cohesion= 100
    --out     = plots/<folder>_timeline_<people>p_c<cohesion>.png
"""

import argparse
import json
import os
import sys

import matplotlib.pyplot as plt

ALGORITHM_COLORS = {
    "annealingFromGrouped":             "tab:blue",
    "annealingFromRandom":              "tab:orange",
    "bruteForce":                       "tab:green",
    "linearSwitchFromGrouped":          "tab:red",
    "linearSwitchFromGroupedProtected": "tab:purple",
    "linearSwitchFromRandom":           "tab:brown",
    "randomSwitchFromGrouped":          "tab:pink",
    "randomSwitchFromRandom":           "tab:gray",
    "tabuSearchFromGrouped":            "tab:olive",
    "tabuSearchFromRandom":             "tab:cyan",
}

SKIP_ALGORITHMS = {
    # "bruteForce",
}


def load_timelines(folder: str, n_people: int, cohesion: int) -> dict[str, list]:
    """Return {algo: first_timeline} for each file in folder."""
    timelines = {}
    people_key = str(n_people)
    cohesion_key = str(cohesion)

    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for algo, algo_data in data.get("results", {}).items():
            if algo in SKIP_ALGORITHMS:
                continue
            if people_key not in algo_data:
                continue
            cohesion_data = algo_data[people_key]
            if cohesion_key not in cohesion_data:
                continue
            all_timelines = cohesion_data[cohesion_key].get("timelines", [])
            if not all_timelines or not all_timelines[0]:
                continue
            # Use first iteration's timeline
            timelines[algo] = all_timelines[0]

    return timelines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="?", default="jsonDataFullRun")
    parser.add_argument("--people", type=int, default=300)
    parser.add_argument("--cohesion", type=int, default=100)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    if args.out is None:
        folder_name = os.path.basename(os.path.normpath(args.folder))
        args.out = f"plots/{folder_name}_timeline_{args.people}p_c{args.cohesion}.png"

    timelines = load_timelines(args.folder, args.people, args.cohesion)
    if not timelines:
        print(f"No timeline data found in '{args.folder}' for "
              f"n_people={args.people}, cohesion={args.cohesion}.", file=sys.stderr)
        sys.exit(1)

    fig, ax = plt.subplots()
    for algo, timeline in sorted(timelines.items()):
        times  = [point[0] for point in timeline]
        scores = [point[1] for point in timeline]
        color = ALGORITHM_COLORS.get(algo, "tab:gray")
        ax.plot(times, scores, label=algo, color=color)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Score")
    ax.set_title(f"Score over time — cohesion={args.cohesion}, {args.people} people")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.tight_layout(rect=[0, 0.01, 1, 1])

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)
    plt.savefig(args.out, dpi=300, bbox_inches="tight")
    print(f"Saved to {args.out}")
    plt.show()


if __name__ == "__main__":
    main()

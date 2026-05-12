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


def load_timelines(folder: str, n_people: int, cohesion: int, iterations: list[int] | None) -> dict[str, list[list]]:
    """Return {algo: [timeline, ...]} for selected iterations for each file in folder."""
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
            if not all_timelines:
                continue
            if iterations is None:
                selected = [all_timelines[0]] if all_timelines[0] else []
            else:
                selected = [all_timelines[i] for i in iterations if i < len(all_timelines) and all_timelines[i]]
            if selected:
                timelines[algo] = selected

    return timelines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="?", default="jsonDataFullRun")
    parser.add_argument("--people", type=int, default=300)
    parser.add_argument("--cohesion", type=int, default=100)
    parser.add_argument("--out", default=None)
    parser.add_argument("--timelimit", type=float, default=None,
                        help="Clip timeline data to this many seconds")
    parser.add_argument("--iterations", type=int, nargs="+", default=None,
                        help="Iteration index or indices to plot, e.g. --iterations 0 or --iterations 0 1 2 (default: 0)")
    args = parser.parse_args()

    if args.out is None:
        folder_name = os.path.basename(os.path.normpath(args.folder))
        timelimit_suffix = f"_t{int(args.timelimit)}" if args.timelimit is not None else ""
        iter_suffix = "_i" + "-".join(str(i) for i in args.iterations) if args.iterations is not None else ""
        args.out = f"plots/{folder_name}_timeline_{args.people}p_c{args.cohesion}{timelimit_suffix}{iter_suffix}.png"

    timelines = load_timelines(args.folder, args.people, args.cohesion, args.iterations)
    if not timelines:
        print(f"No timeline data found in '{args.folder}' for "
              f"n_people={args.people}, cohesion={args.cohesion}.", file=sys.stderr)
        sys.exit(1)

    fig, ax = plt.subplots()
    endpoints = []  # (last_time, last_score, color)
    for algo, algo_timelines in sorted(timelines.items()):
        color = ALGORITHM_COLORS.get(algo, "tab:gray")
        for idx, timeline in enumerate(algo_timelines):
            times  = [point[0] for point in timeline]
            scores = [point[1] for point in timeline]
            if args.timelimit is not None:
                pairs = [(t, s) for t, s in zip(times, scores) if t <= args.timelimit]
                times, scores = (list(x) for x in zip(*pairs)) if pairs else ([], [])
            label = algo if idx == 0 else "_nolegend_"
            ax.plot(times, scores, label=label, color=color)
            if times:
                endpoints.append((times[-1], scores[-1], color))

    x_max = ax.get_xlim()[1]
    for last_time, last_score, color in endpoints:
        ax.plot([last_time, x_max], [last_score, last_score],
                color=color, linestyle="--", linewidth=1, alpha=0.6)

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

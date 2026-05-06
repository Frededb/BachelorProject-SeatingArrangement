"""
Plot mean score vs cohesion for each algorithm from a folder of JSON result files.

Usage:
    python createPlot.py [folder] [--people N] [--timelimit T] [--out FILE]

Defaults:
    folder     = jsonDataTimeComp
    --people   = 300
    --timelimit = last available (ignored if data has no timelimit dimension)
    --out      = plots/<folder>_plot.png
"""

import argparse
import json
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

ALGORITHM_COLORS = {
    "annealingFromFluent":           "tab:blue",
    "annealingFromRandom":           "tab:orange",
    "bruteForce":                    "tab:green",
    "linearSwitchFromFluent":        "tab:red",
    "linearSwitchFromFluentProtected": "tab:purple",
    "linearSwitchFromRandom":        "tab:brown",
    "randomSwitchFromFluent":        "tab:pink",
    "randomSwitchFromRandom":        "tab:gray",
    "tabuSearchFromFluent":          "tab:olive",
    "tabuSearchFromRandom":          "tab:cyan",
}


def load_folder(folder: str, n_people: int, timelimit_key: str | None) -> pd.DataFrame:
    rows = []
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for algo, algo_data in data.get("results", {}).items():
            # Detect whether timelimit is an outer dimension.
            # Heuristic: if first key is numeric string it's a timelimit.
            first_key = next(iter(algo_data))
            try:
                float(first_key)
                has_timelimit = True
            except ValueError:
                has_timelimit = False

            if has_timelimit:
                available = list(algo_data.keys())
                tl = timelimit_key if timelimit_key in available else available[-1]
                people_data = algo_data[tl]
            else:
                people_data = algo_data

            people_key = str(n_people)
            if people_key not in people_data:
                continue

            for cohesion_str, entry in people_data[people_key].items():
                avg = entry.get("avg_score")
                if avg is None and entry.get("scores"):
                    scores = [s for s in entry["scores"] if isinstance(s, (int, float))]
                    avg = sum(scores) / len(scores) if scores else None
                if avg is not None:
                    rows.append({
                        "algorithm": algo,
                        "cohesion": int(cohesion_str),
                        "mean_score": avg,
                    })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Plot score vs cohesion from JSON result folder.")
    parser.add_argument("folder", nargs="?", default="jsonDataTimeComp")
    parser.add_argument("--people", type=int, default=300)
    parser.add_argument("--timelimit", type=str, default=None,
                        help="Timelimit key to use (e.g. '20'). Defaults to last available.")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    if args.out is None:
        folder_name = os.path.basename(os.path.normpath(args.folder))
        args.out = f"plots/{folder_name}_plot.png"

    df = load_folder(args.folder, args.people, args.timelimit)
    if df.empty:
        print(f"No data found in '{args.folder}' for n_people={args.people}.", file=sys.stderr)
        sys.exit(1)

    pivot = df.pivot_table(index="cohesion", columns="algorithm", values="mean_score")
    colors = {algo: ALGORITHM_COLORS.get(algo, "tab:gray") for algo in pivot.columns}

    fig, ax = plt.subplots()
    pivot.plot(ax=ax, marker="o", color=colors,
               title=f"Performance with {args.people} people ({os.path.basename(args.folder)})",
               xlabel="Cohesion", ylabel="Mean Score")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.tight_layout(rect=[0, 0.01, 1, 1])

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)
    plt.savefig(args.out, dpi=300, bbox_inches="tight")
    print(f"Saved to {args.out}")
    plt.show()


if __name__ == "__main__":
    main()

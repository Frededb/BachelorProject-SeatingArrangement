"""
Plot mean score vs cohesion for each algorithm from a folder of JSON result files.

Usage:
    python createPlot.py [folder] [--people N] [--out FILE]

Defaults:
    folder   = jsonDataComposite
    --people = 300
    --out    = plots/<folder>_plot.png
"""

import argparse
import json
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

SKIP_ALGORITHMS = {
    # "bruteForce",
    # "theoreticalMax",
}

ALGORITHM_COLORS = {
    "annealingFromGrouped":           "tab:blue",
    "annealingFromRandom":           "tab:orange",
    "bruteForce":                    "tab:green",
    "linearSwitchFromGrouped":        "tab:red",
    "linearSwitchFromGroupedProtected": "tab:purple",
    "linearSwitchFromRandom":        "tab:brown",
    "randomSwitchFromGrouped":        "tab:pink",
    "randomSwitchFromRandom":        "tab:gray",
    "tabuSearchFromGrouped":          "tab:olive",
    "tabuSearchFromRandom":          "tab:cyan",
}


def load_folder(folder: str, n_people: int) -> pd.DataFrame:
    rows = []
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for algo, algo_data in data.get("results", {}).items():
            if algo in SKIP_ALGORITHMS:
                continue
            people_key = str(n_people)
            if people_key not in algo_data:
                continue

            for cohesion_str, entry in algo_data[people_key].items():
                avg = entry.get("avg_score")
                if not isinstance(avg, (int, float)):
                    avg = None
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
    parser.add_argument("folder", nargs="?", default="jsonDataComposite")
    parser.add_argument("--people", type=int, default=300)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    if args.out is None:
        folder_name = os.path.basename(os.path.normpath(args.folder))
        args.out = f"plots/{folder_name}_plot{args.people}.png"

    df = load_folder(args.folder, args.people)
    if df.empty:
        print(f"No data found in '{args.folder}' for n_people={args.people}.", file=sys.stderr)
        sys.exit(1)

    pivot = df.pivot_table(index="cohesion", columns="algorithm", values="mean_score")
    colors = {algo: ALGORITHM_COLORS.get(algo, "tab:gray") for algo in pivot.columns}

    fig, ax = plt.subplots()
    pivot.plot(ax=ax, marker="o", color=colors,
               title=f"Performance with {args.people} people",
               xlabel="Cohesion", ylabel="Mean Score")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.tight_layout(rect=[0, 0.01, 1, 1])

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)
    plt.savefig(args.out, dpi=300, bbox_inches="tight")
    print(f"Saved to {args.out}")
    plt.show()


if __name__ == "__main__":
    main()

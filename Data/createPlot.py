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


def load_folder(folder: str, n_people: int | None, max_iterations: int | None = None) -> pd.DataFrame:
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

            for people_str, cohesion_data in algo_data.items():
                if n_people is not None and int(people_str) != n_people:
                    continue
                for cohesion_str, entry in cohesion_data.items():
                    avg = entry.get("avg_score")
                    if not isinstance(avg, (int, float)):
                        avg = None
                    if avg is None and entry.get("scores"):
                        scores = [s for s in entry["scores"] if isinstance(s, (int, float))]
                        if max_iterations is not None:
                            scores = scores[:max_iterations]
                        avg = sum(scores) / len(scores) if scores else None
                    if avg is not None:
                        rows.append({
                            "algorithm": algo,
                            "n_people": int(people_str),
                            "cohesion": int(cohesion_str),
                            "mean_score": avg,
                        })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Plot score vs cohesion from JSON result folder.")
    parser.add_argument("folder", nargs="?", default="jsonDataComposite")
    parser.add_argument("--people", type=int, default=None)
    parser.add_argument("--iterations", type=int, default=None,
                        help="Only use the first N iterations (default: all)")
    parser.add_argument("--xaxis", choices=["cohesion", "people"], default="cohesion",
                        help="What to use as x-axis (default: cohesion)")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    if args.out is None:
        folder_name = os.path.basename(os.path.normpath(args.folder))
        suffix = args.people if args.people else "all"
        iter_suffix = f"_i{args.iterations}" if args.iterations is not None else ""
        args.out = f"plots/{folder_name}_{args.xaxis}{suffix}{iter_suffix}.png"

    df = load_folder(args.folder, args.people, args.iterations)
    if df.empty:
        print(f"No data found in '{args.folder}'.", file=sys.stderr)
        sys.exit(1)

    if args.xaxis == "people":
        pivot = df.pivot_table(index="n_people", columns="algorithm", values="mean_score")
        xlabel = "Number of people"
        title_detail = f"averaged over cohesion"
    else:
        if args.people is None:
            print("--people is required when --xaxis=cohesion", file=sys.stderr)
            sys.exit(1)
        pivot = df[df["n_people"] == args.people].pivot_table(
            index="cohesion", columns="algorithm", values="mean_score"
        )
        xlabel = "Cohesion"
        title_detail = f"{args.people} people"
    colors = {algo: ALGORITHM_COLORS.get(algo, "tab:gray") for algo in pivot.columns}

    fig, ax = plt.subplots()
    pivot.plot(ax=ax, marker="o", color=colors,
               title=f"Performance — {title_detail}",
               xlabel=xlabel, ylabel="Mean Score")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.tight_layout(rect=[0, 0.01, 1, 1])

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)
    plt.savefig(args.out, dpi=300, bbox_inches="tight")
    print(f"Saved to {args.out}")
    plt.show()


if __name__ == "__main__":
    main()

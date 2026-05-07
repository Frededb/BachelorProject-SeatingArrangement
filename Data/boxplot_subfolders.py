"""
Boxplot of scores per cohesion from a folder of subfolders, each containing JSON result files.
All numeric scores across all subfolders are merged per cohesion.

Usage:
    python boxplot_subfolders.py [folder] [--people N] [--out FILE]

Defaults:
    folder   = ../hpc-jobs/outputs/job74058
    --people = 100
    --out    = plots/<folder>_boxplot.png
"""

import argparse
import json
import os
import sys
from collections import defaultdict

import matplotlib.pyplot as plt


def collect_scores(folder: str, n_people: int) -> dict[int, list[float]]:
    """Return {cohesion: [all individual scores]} merged from all subfolders."""
    scores_by_cohesion: dict[int, list[float]] = defaultdict(list)
    people_key = str(n_people)

    for entry in sorted(os.scandir(folder), key=lambda e: e.name):
        if not entry.is_dir():
            continue
        for fname in sorted(os.listdir(entry.path)):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(entry.path, fname)
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            for algo, algo_data in data.get("results", {}).items():
                # Detect timelimit outer dimension (numeric first key)
                first_key = next(iter(algo_data))
                try:
                    float(first_key)
                    people_data = algo_data[first_key]   # use first timelimit
                    # prefer last timelimit (longest run)
                    last_key = list(algo_data.keys())[-1]
                    people_data = algo_data[last_key]
                except ValueError:
                    people_data = algo_data

                if people_key not in people_data:
                    continue

                for cohesion_str, cohesion_entry in people_data[people_key].items():
                    raw = cohesion_entry.get("scores", [])
                    numeric = [s for s in raw if isinstance(s, (int, float))]
                    scores_by_cohesion[int(cohesion_str)].extend(numeric)

    return scores_by_cohesion


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="?", default="../hpc-jobs/outputs/job74058")
    parser.add_argument("--people", type=int, default=100)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    if args.out is None:
        folder_name = os.path.basename(os.path.normpath(args.folder))
        args.out = f"plots/{folder_name}_boxplot.png"

    scores_by_cohesion = collect_scores(args.folder, args.people)
    if not scores_by_cohesion:
        print(f"No data found in '{args.folder}' for n_people={args.people}.", file=sys.stderr)
        sys.exit(1)

    cohesions = sorted(scores_by_cohesion.keys())
    data = [scores_by_cohesion[c] for c in cohesions]

    fig, ax = plt.subplots()
    ax.boxplot(data, labels=cohesions, patch_artist=True)
    ax.set_xlabel("Cohesion")
    ax.set_ylabel("Score")
    folder_name = os.path.basename(os.path.normpath(args.folder))
    ax.set_title(f"Score distribution by cohesion — {folder_name} ({args.people} people)")
    plt.tight_layout()

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)
    plt.savefig(args.out, dpi=300, bbox_inches="tight")
    print(f"Saved to {args.out}")
    plt.show()


if __name__ == "__main__":
    main()

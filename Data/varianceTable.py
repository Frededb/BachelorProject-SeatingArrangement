"""
Print a variance table for each algorithm from a folder of JSON result files.

Columns: Algorithm | Avg Score | Mean CV | Max CV

CV (Coefficient of Variation) = std / mean for each cohesion level's 10 scores,
then averaged / maximised across all cohesion levels.

Usage:
    python varianceTable.py [folder] [--people N] [--out FILE]

Defaults:
    folder   = jsonDataFullRun
    --people = 300
    --out    = (print to stdout only)
"""

import argparse
import json
import math
import os
import sys


def load_folder(folder: str, n_people: int) -> dict[str, dict[str, list[float]]]:
    """Return {algo: {cohesion: [scores]}} skipping DNF values."""
    data = {}
    people_key = str(n_people)

    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding="utf-8") as f:
            d = json.load(f)

        for algo, algo_data in d.get("results", {}).items():
            if people_key not in algo_data:
                continue
            for cohesion_str, entry in algo_data[people_key].items():
                scores = [s for s in entry.get("scores", []) if isinstance(s, (int, float))]
                if not scores:
                    continue
                data.setdefault(algo, {}).setdefault(cohesion_str, []).extend(scores)

    return data


def cv(scores: list[float]) -> float | None:
    n = len(scores)
    if n < 2:
        return None
    mean = sum(scores) / n
    if mean == 0:
        return None
    variance = sum((s - mean) ** 2 for s in scores) / (n - 1)
    return math.sqrt(variance) / mean


def build_rows(data: dict) -> list[dict]:
    rows = []
    for algo, cohesion_map in sorted(data.items()):
        all_scores = [s for scores in cohesion_map.values() for s in scores]
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

        cvs = [c for c in (cv(scores) for scores in cohesion_map.values()) if c is not None]
        mean_cv = sum(cvs) / len(cvs) if cvs else 0
        max_cv = max(cvs) if cvs else 0

        rows.append({
            "algorithm": algo,
            "avg_score": avg_score,
            "mean_cv": mean_cv,
            "max_cv": max_cv,
        })

    rows.sort(key=lambda r: r["avg_score"], reverse=True)
    return rows


def print_table(rows: list[dict], out=sys.stdout):
    header = f"{'Algorithm':<35} {'Avg Score':>12} {'Mean CV':>10} {'Max CV':>10}"
    print(header, file=out)
    print("-" * len(header), file=out)
    for r in rows:
        print(
            f"{r['algorithm']:<35} {r['avg_score']:>12.1f}"
            f" {r['mean_cv']:>9.4f}  {r['max_cv']:>9.4f}",
            file=out,
        )


def write_csv(rows: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("algorithm,avg_score,mean_cv,max_cv\n")
        for r in rows:
            f.write(f"{r['algorithm']},{r['avg_score']:.4f},{r['mean_cv']:.6f},{r['max_cv']:.6f}\n")
    print(f"CSV saved to {path}")


def main():
    parser = argparse.ArgumentParser(description="Variance table for seating algorithms.")
    parser.add_argument("folder", nargs="?", default="jsonDataFullRun")
    parser.add_argument("--people", type=int, default=300)
    parser.add_argument("--out", default=None, help="Optional path to write CSV output")
    args = parser.parse_args()

    d = load_folder(args.folder, args.people)
    if not d:
        print(f"No data found in '{args.folder}'.", file=sys.stderr)
        sys.exit(1)

    rows = build_rows(d)
    print_table(rows)
    if args.out:
        write_csv(rows, args.out)


if __name__ == "__main__":
    main()

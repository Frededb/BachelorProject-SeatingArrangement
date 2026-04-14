from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

PersonLinks = Dict[str, Dict[str, Set[str]]]


def _sanitize_links(names: Set[str], owner: str, links: Iterable[Any]) -> Set[str]:
    """Keep only known names and remove self-links."""
    cleaned = set()
    for value in links or []:
        if isinstance(value, str) and value in names and value != owner:
            cleaned.add(value)
    return cleaned


def load_people_from_data(data: List[Dict[str, Any]]) -> PersonLinks:
    """Normalize raw JSON rows into a name -> {preferences, avoidances} mapping."""
    names: Set[str] = set()
    for row in data:
        if isinstance(row, dict) and isinstance(row.get("name"), str):
            names.add(row["name"])

    people: PersonLinks = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        if not isinstance(name, str):
            continue

        people[name] = {
            "preferences": _sanitize_links(names, name, row.get("preferences", [])),
            "avoidances": _sanitize_links(names, name, row.get("avoidances", [])),
        }

    return people


def load_people_from_file(file_path: str | Path) -> PersonLinks:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of people.")

    return load_people_from_data(data)


def resolve_input_path(input_path: str | Path) -> Path:
    """Resolve non-absolute input paths relative to the Inputs folder."""
    candidate = Path(input_path)
    if candidate.is_absolute():
        return candidate

    inputs_dir = Path(__file__).resolve().parent
    return (inputs_dir / candidate).resolve()


def _ratio(numerator: int, denominator: int) -> Dict[str, Any]:
    percentage = ((numerator / denominator) * 100) if denominator else None
    return {
        "numerator": numerator,
        "denominator": denominator,
        "percentage": percentage,
    }


def _distribution_with_percentages(counter: Counter, total: int) -> Dict[str, Dict[Any, Any]]:
    counts = dict(sorted(counter.items()))
    percentages = {
        key: ((value / total) * 100) if total else 0.0
        for key, value in counts.items()
    }
    return {
        "counts": counts,
        "percentages": percentages,
    }


def chance_b_prefers_a_given_a_prefers_b(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["preferences"]:
            denominator += 1
            if a in people[b]["preferences"]:
                numerator += 1
    return _ratio(numerator, denominator)


def chance_b_avoids_a_given_a_avoids_b(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["avoidances"]:
            denominator += 1
            if a in people[b]["avoidances"]:
                numerator += 1
    return _ratio(numerator, denominator)


def chance_b_avoids_a_given_a_prefers_b(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["preferences"]:
            denominator += 1
            if a in people[b]["avoidances"]:
                numerator += 1
    return _ratio(numerator, denominator)


def chance_b_prefers_a_given_a_avoids_b(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["avoidances"]:
            denominator += 1
            if a in people[b]["preferences"]:
                numerator += 1
    return _ratio(numerator, denominator)


def chance_a_prefers_c_given_a_prefers_b_and_b_prefers_c(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["preferences"]:
            for c in people[b]["preferences"]:
                if c == a:
                    continue
                denominator += 1
                if c in links["preferences"]:
                    numerator += 1
    return _ratio(numerator, denominator)


def chance_a_avoids_c_given_a_prefers_b_and_b_avoids_c(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["preferences"]:
            for c in people[b]["avoidances"]:
                if c == a:
                    continue
                denominator += 1
                if c in links["avoidances"]:
                    numerator += 1
    return _ratio(numerator, denominator)


def chance_a_prefers_c_given_a_prefers_b_and_b_avoids_c(people: PersonLinks) -> Dict[str, Any]:
    numerator = 0
    denominator = 0
    for a, links in people.items():
        for b in links["preferences"]:
            for c in people[b]["avoidances"]:
                if c == a:
                    continue
                denominator += 1
                if c in links["preferences"]:
                    numerator += 1
    return _ratio(numerator, denominator)


def chance_a_prefers_d_given_a_prefers_b_and_c_and_b_and_c_prefer_d(
    people: PersonLinks,
) -> Dict[str, Any]:
    numerator = 0
    denominator = 0

    for a, links in people.items():
        for b, c in combinations(sorted(links["preferences"]), 2):
            common_targets = people[b]["preferences"].intersection(people[c]["preferences"])
            for d in common_targets:
                if d == a:
                    continue
                denominator += 1
                if d in links["preferences"]:
                    numerator += 1

    return _ratio(numerator, denominator)


def outgoing_distributions(people: PersonLinks) -> Dict[str, Any]:
    """Distribution based on sanitized links used in graph calculations."""
    prefers = Counter(len(links["preferences"]) for links in people.values())
    avoids = Counter(len(links["avoidances"]) for links in people.values())
    total_people = len(people)
    return {
        "prefers_distribution": _distribution_with_percentages(prefers, total_people),
        "avoids_distribution": _distribution_with_percentages(avoids, total_people),
    }


def declared_outgoing_distributions_from_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Distribution based on declared JSON lists before sanitizing unknown names."""
    prefers = Counter()
    avoids = Counter()

    for row in data:
        if not isinstance(row, dict):
            continue

        preferences = row.get("preferences", [])
        avoidances = row.get("avoidances", [])

        prefers[len(preferences) if isinstance(preferences, list) else 0] += 1
        avoids[len(avoidances) if isinstance(avoidances, list) else 0] += 1

    total_people = sum(prefers.values())
    return {
        "prefers_distribution": _distribution_with_percentages(prefers, total_people),
        "avoids_distribution": _distribution_with_percentages(avoids, total_people),
    }


def studyprogram_and_year_distributions_from_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    studyprograms = Counter()
    years = Counter()

    for row in data:
        if not isinstance(row, dict):
            continue

        studyprogram = row.get("studyprogram")
        year = row.get("year")

        if isinstance(studyprogram, str) and studyprogram:
            studyprograms[studyprogram] += 1
        if isinstance(year, str) and year:
            years[year] += 1

    total_people = sum(studyprograms.values())
    return {
        "studyprogram_distribution": _distribution_with_percentages(studyprograms, total_people),
        "year_distribution": _distribution_with_percentages(years, total_people),
    }


def _save_pie_chart(counts: Dict[Any, Any], title: str, output_path: Path) -> None:
    if not counts:
        return

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError(
            "Saving charts requires matplotlib. Install it with: pip install matplotlib"
        ) from exc

    labels = [str(label) for label in counts.keys()]
    values = [counts[label] for label in counts.keys()]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_demographic_pie_charts(result: Dict[str, Any], output_dir: Path) -> Dict[str, str]:
    demo = result.get("demographic_distributions", {})
    studyprogram_counts = demo.get("studyprogram_distribution", {}).get("counts", {})
    year_counts = demo.get("year_distribution", {}).get("counts", {})

    studyprogram_chart = output_dir / "studyprogram_pie.png"
    year_chart = output_dir / "year_pie.png"

    _save_pie_chart(studyprogram_counts, "Study Program Distribution", studyprogram_chart)
    _save_pie_chart(year_counts, "Year Distribution", year_chart)

    return {
        "studyprogram_pie": str(studyprogram_chart),
        "year_pie": str(year_chart),
    }


def incoming_distributions(people: PersonLinks) -> Dict[str, Any]:
    preferred_by_count = {name: 0 for name in people}
    avoided_by_count = {name: 0 for name in people}

    for links in people.values():
        for target in links["preferences"]:
            preferred_by_count[target] += 1
        for target in links["avoidances"]:
            avoided_by_count[target] += 1

    preferred_dist = Counter(preferred_by_count.values())
    avoided_dist = Counter(avoided_by_count.values())
    total_people = len(people)

    return {
        "preferred_by_x_people_distribution": _distribution_with_percentages(preferred_dist, total_people),
        "avoided_by_x_people_distribution": _distribution_with_percentages(avoided_dist, total_people),
    }


def run_all_analyses(people: PersonLinks) -> Dict[str, Any]:
    return {
        "people_count": len(people),
        "conditional_probabilities": {
            "P(B_prefers_A | A_prefers_B)": chance_b_prefers_a_given_a_prefers_b(people),
            "P(B_avoids_A | A_avoids_B)": chance_b_avoids_a_given_a_avoids_b(people),
            "P(B_avoids_A | A_prefers_B)": chance_b_avoids_a_given_a_prefers_b(people),
            "P(B_prefers_A | A_avoids_B)": chance_b_prefers_a_given_a_avoids_b(people),
            "P(A_prefers_C | A_prefers_B and B_prefers_C)": chance_a_prefers_c_given_a_prefers_b_and_b_prefers_c(people),
            "P(A_avoids_C | A_prefers_B and B_avoids_C)": chance_a_avoids_c_given_a_prefers_b_and_b_avoids_c(people),
            "P(A_prefers_C | A_prefers_B and B_avoids_C)": chance_a_prefers_c_given_a_prefers_b_and_b_avoids_c(people),
            "P(A_prefers_D | A_prefers_B and A_prefers_C and B_prefers_D and C_prefers_D)": chance_a_prefers_d_given_a_prefers_b_and_c_and_b_and_c_prefer_d(people),
        },
        "outgoing_distributions": outgoing_distributions(people),
        "incoming_distributions": incoming_distributions(people),
    }


def run_all_analyses_from_file(file_path: str | Path) -> Dict[str, Any]:
    resolved_path = resolve_input_path(file_path)

    with open(resolved_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of people.")

    people = load_people_from_data(data)
    result = run_all_analyses(people)
    result["declared_outgoing_distributions"] = declared_outgoing_distributions_from_data(data)
    result["demographic_distributions"] = studyprogram_and_year_distributions_from_data(data)
    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze preference/avoidance patterns in input JSON")
    parser.add_argument("input_json", help="Path to input JSON file")
    parser.add_argument("--indent", type=int, default=2, help="JSON output indentation")
    parser.add_argument(
        "--save-charts",
        action="store_true",
        help="Save pie charts for study program and year distributions",
    )
    parser.add_argument(
        "--charts-dir",
        default="charts",
        help="Output folder for charts, relative to Inputs if not absolute",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = run_all_analyses_from_file(args.input_json)

    if args.save_charts:
        charts_dir = Path(args.charts_dir)
        if not charts_dir.is_absolute():
            charts_dir = Path(__file__).resolve().parent / charts_dir

        dataset_name = resolve_input_path(args.input_json).stem
        chart_paths = save_demographic_pie_charts(result, charts_dir / dataset_name)
        result["chart_paths"] = chart_paths

    print(json.dumps(result, indent=args.indent))


if __name__ == "__main__":
    main()


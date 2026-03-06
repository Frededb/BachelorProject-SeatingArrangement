import os
import sys

# Ensure project root on sys.path so imports work when module is imported/run
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Utils.ValueCalc import calcTable


def makeGraphFromInput(people):
    """Build a simple undirected weighted graph from a list of Person objects.

    Input: `people` should be the list returned by `Utils.reader.readjson(...)` (i.e. a list
    of `Utils.Person.Person` objects).

    Returns: adjacency dict {name: {neighbor_name: weight, ...}, ...}
    where weight = calcTable([personA, personB])[0].
    """

    name_to_person = {p.name: p for p in people}
    names = list(name_to_person.keys())
    graph = {n: {} for n in names}

    # Compute each unordered pair once and mirror the value
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = name_to_person[names[i]]
            b = name_to_person[names[j]]
            try:
                weight, _ = calcTable([a, b])
            except Exception:
                weight = 0
            graph[names[i]][names[j]] = weight
            graph[names[j]][names[i]] = weight

    return graph


def print_graph(graph, max_neighbors=None, min_weight=None, sort_by_weight=False):
    """Print adjacency dict in a readable way.

    Parameters:
    - graph: {name: {neighbor: weight, ...}, ...}
    - max_neighbors: if set, only print up to this many neighbors per node (largest weights first if sort_by_weight True)
    - min_weight: if set, only print neighbors with weight >= min_weight
    - sort_by_weight: if True, sort neighbors by descending weight; otherwise sort by name
    """
    for name, neighbors in graph.items():
        print(f"{name}:")
        items = list(neighbors.items())
        if min_weight is not None:
            items = [(n, w) for (n, w) in items if w >= min_weight]
        if sort_by_weight:
            items.sort(key=lambda x: x[1], reverse=True)
        else:
            items.sort(key=lambda x: x[0])
        if max_neighbors is not None:
            items = items[:max_neighbors]
        if not items:
            print("  (no neighbors)")
            continue
        for nb, w in items:
            print(f"  -> {nb}: {w}")

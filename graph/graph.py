import os
import sys

# Ensure project root on sys.path so imports work when module is imported/run
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Utils.bmalls import getPersonsByName


def makeGraphFromInput(people):
    """Build a simple undirected weighted graph from Person objects.

    Returns: adjacency dict {name: {neighbor_name: weight, ...}, ...}
    where pair weight is the net sentiment across both directions:
    +1 for each directed preference, -1 for each directed avoidance.

    Example for pair (A, B):
    weight = [A prefers B] + [B prefers A] - [A avoids B] - [B avoids A]
    """

    name_to_person = {p.name: p for p in people}
    names = list(name_to_person.keys())
    graph = {n: {} for n in names}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = name_to_person[names[i]]
            b = name_to_person[names[j]]

            a_prefs = set(getattr(a, "preferences", []) or [])
            a_avoids = set(getattr(a, "avoidances", []) or [])
            b_prefs = set(getattr(b, "preferences", []) or [])
            b_avoids = set(getattr(b, "avoidances", []) or [])

            pref_count = int(b.name in a_prefs) + int(a.name in b_prefs)
            avoid_count = int(b.name in a_avoids) + int(a.name in b_avoids)
            weight = pref_count - avoid_count

            # Fully canceled pairs have no edge.
            if weight == 0:
                continue

            graph[a.name][b.name] = weight
            graph[b.name][a.name] = weight

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


def _induced_subgraph(graph, nodes):
    """Return adjacency dict induced by nodes (subset of names)."""
    return {u: {v: w for v, w in nbrs.items() if v in nodes} for u, nbrs in graph.items() if u in nodes}


def _best_balanced_cut(graph):
    """Run Stoer-Wagner but return the most balanced cut (by size) among all candidate cuts.

    Instead of the globally minimum cut (which tends to peel off single nodes),
    score each cut by cut_weight / min(|A|, |B|) and pick the one with the lowest score.
    This strongly prefers cuts that split the graph roughly in half.

    Returns: (cut_weight, (set_A, set_B))
    """
    adj = {u: dict(neigh) for u, neigh in graph.items()}
    v_sets = {u: {u} for u in adj.keys()}
    vertices = list(adj.keys())

    best_score = float('inf')
    best_partition = (set(), set())
    best_cut = float('inf')

    while len(vertices) > 1:
        weights = {v: 0.0 for v in vertices}
        added = []
        for i in range(len(vertices)):
            sel = max((v for v in vertices if v not in added), key=lambda x: weights[x])
            added.append(sel)
            if i < len(vertices) - 1:
                for v in vertices:
                    if v not in added:
                        weights[v] += adj[sel].get(v, 0.0)
            else:
                t = sel
                s = added[-2]
                cut_weight = weights[t]

                S = set()
                for v in added[:-1]:
                    S |= v_sets[v]
                all_nodes = set().union(*v_sets.values())
                T = all_nodes - S

                # Score: cut_weight / (|A| * |B|) — sparsest cut metric.
                # Low score = sparse connection between A and B = good split.
                score = cut_weight / (len(S) * len(T))
                if score < best_score:
                    best_score = score
                    best_partition = (S, T)
                    best_cut = cut_weight

                # merge t into s
                for v in vertices:
                    if v == s or v == t:
                        continue
                    adj[s][v] = adj[s].get(v, 0.0) + adj[t].get(v, 0.0)
                    adj[v][s] = adj[s][v]
                vertices.remove(t)
                adj.pop(t, None)
                for v in adj:
                    adj[v].pop(t, None)
                v_sets[s] |= v_sets[t]
                v_sets.pop(t, None)
                break

    return best_cut, best_partition


def find_connected_components(graph):
    """Find connected components following only positive-weight edges."""
    visited = set()
    components = []
    for start in graph:
        if start in visited:
            continue
        comp = set()
        queue = [start]
        while queue:
            node = queue.pop()
            if node in visited:
                continue
            visited.add(node)
            comp.add(node)
            for nb, w in graph[node].items():
                if w > 0 and nb not in visited:
                    queue.append(nb)
        components.append(comp)

    return components


def find_groups(graph, people, weight_threshold=None, max_groups=None, verbose=False):
    """Find groups by splitting on connected components, then balanced min-cuts.

    Parameters:
    - graph: adjacency dict from makeGraphFromInput.
    - people: original list of Person objects (from reader.readjson).
    - weight_threshold: only accept a split when score (cut_weight / (|A|*|B|)) <= weight_threshold.
    - max_groups: stop once this many groups have been produced.
    - verbose: print cut info at each step.

    Returns: list of sets of Person objects.
    """
    groups = []

    def _rec(nodes):
        if max_groups is not None and len(groups) >= max_groups:
            groups.append(set(nodes))
            return

        sub = _induced_subgraph(graph, nodes)

        # First split by connected components — isolates nodes with no edges immediately
        components = find_connected_components(sub)
        if len(components) > 1:
            for comp in components:
                _rec(comp)
            return

        # Single node — done
        if len(nodes) == 1:
            groups.append(set(nodes))
            return

        # Run balanced min-cut directly on the signed graph.
        # Negative edges (avoidances) make those cuts cheaper, so avoiders naturally separate.
        cut_weight, (A, B) = _best_balanced_cut(sub)

        score = cut_weight / (len(A) * len(B))


        if verbose:
            print(f"Cut: weight={cut_weight:.1f}, |A|={len(A)}, |B|={len(B)}, score={score:.4f}")

        if weight_threshold is not None and score > weight_threshold:
            if verbose:
                print(f"Reject: score {score:.4f} > threshold {weight_threshold}")
            groups.append(set(nodes))
            return

        _rec(A)
        _rec(B)

    _rec(set(graph.keys()))
    # Convert name sets to Person object sets
    return [getPersonsByName(group, people) for group in groups]



def print_groups(groups):
    """Pretty-print a list of groups (each group is a set of Person objects)."""
    for i, g in enumerate(groups, start=1):
        print(f"Group {i} (size {len(g)}):")
        for person in sorted(g, key=lambda p: p.name):
            print(f"  - {person.name}")
        print()

def splitGroupsByMaxSize(graph, input, maxGroupSize):
    pending = find_groups(graph, input, weight_threshold=0)
    newGroups = []

    while pending:
        group = pending.pop(0)

        if len(group) <= maxGroupSize:
            newGroups.append(group)
            continue

        groupGraph = makeGraphFromInput(group)

        # Try increasingly permissive thresholds until a real split is found.
        for i in range(100):
            threshold = i / 10
            smallerGroups = find_groups(groupGraph, input, weight_threshold=threshold)

            # Ignore results that did not split the group.
            if len(smallerGroups) <= 1:
                continue

            for smallerGroup in smallerGroups:
                if len(smallerGroup) <= maxGroupSize:
                    newGroups.append(smallerGroup)
                else:
                    pending.append(set(smallerGroup))
            break

        else:
            print("EROOR GROUP DID NOT SPLIT: ", group)

    return newGroups
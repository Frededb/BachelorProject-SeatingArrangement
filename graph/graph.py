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
    names = sorted(name_to_person.keys())
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


def _best_min_cut(graph):
    """Run Stoer-Wagner and return the global minimum cut.

    Returns: (cut_weight, (set_A, set_B)).
    If multiple cuts share the same weight, prefer the one with the smaller side
    to encourage peeling one/few nodes when ties happen.
    """
    adj = {u: dict(neigh) for u, neigh in graph.items()}
    v_sets = {u: {u} for u in adj.keys()}
    vertices = sorted(adj.keys())

    best_partition = (set(), set())
    best_cut = float('inf')

    while len(vertices) > 1:
        weights = {v: 0.0 for v in vertices}
        added = []
        for i in range(len(vertices)):
            sel = max((v for v in vertices if v not in added), key=lambda x: (weights[x], x))
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

                if (
                    cut_weight < best_cut
                    or (
                        cut_weight == best_cut
                        and min(len(S), len(T)) < min(len(best_partition[0]), len(best_partition[1]))
                    )
                ):
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
    for start in sorted(graph.keys()):
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
            for nb, w in sorted(graph[node].items(), key=lambda item: item[0]):
                if w > 0 and nb not in visited:
                    queue.append(nb)
        components.append(comp)

    return components


def find_groups(graph, people, weight_threshold=None, max_groups=None, verbose=False):
    """Find groups by splitting on connected components, then global min-cuts.

    Parameters:
    - graph: adjacency dict from makeGraphFromInput.
    - people: original list of Person objects (from reader.readjson).
    - weight_threshold: only accept a split when cut_weight <= weight_threshold.
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
            components.sort(key=lambda comp: tuple(sorted(comp)))
            for comp in components:
                _rec(comp)
            return

        # Single node — done
        if len(nodes) == 1:
            groups.append(set(nodes))
            return

        # Run global min-cut directly on the signed graph.
        # Negative edges (avoidances) make those cuts cheaper, so avoiders naturally separate.
        cut_weight, (A, B) = _best_min_cut(sub)


        if verbose:
            print(f"Cut: weight={cut_weight:.4f}, |A|={len(A)}, |B|={len(B)}")

        if weight_threshold is not None and cut_weight > weight_threshold:
            if verbose:
                print(f"Reject: cut_weight {cut_weight:.4f} > threshold {weight_threshold}")
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


def _jitter_graph(graph, epsilon=0.75):
    """Add tiny deterministic symmetric noise to edge weights to break perfect ties."""
    names = sorted(graph.keys())
    jittered = {name: {} for name in names}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]
            if b not in graph[a]:
                continue
            # Deterministic pseudo-noise from pair index (stable across runs).
            raw = ((i + 1) * 131 + (j + 1) * 17) % 2001
            delta = ((raw / 1000.0) - 1.0) * epsilon
            weight = graph[a][b] + delta
            jittered[a][b] = weight
            jittered[b][a] = weight

    return jittered


def splitGroupsByMaxSize(graph, input, maxGroupSize):
    pending = find_groups(graph, input, weight_threshold=0)
    pending.sort(key=lambda group: tuple(sorted(person.name for person in group)))
    newGroups = []

    while pending:
        group = pending.pop(0)

        if len(group) <= maxGroupSize:
            newGroups.append(group)
            continue

        ordered_group = sorted(list(group), key=lambda person: person.name)
        groupGraph = makeGraphFromInput(ordered_group)
        group_size = len(ordered_group)
        required_leave = group_size - maxGroupSize

        def pick_chunk(split):
            best_size = -1
            best_names = None
            for subgroup in split:
                size = len(subgroup)
                if size == 0 or size > maxGroupSize or group_size - size < required_leave:
                    continue
                names = tuple(sorted(person.name for person in subgroup))
                if size > best_size or (size == best_size and (best_names is None or names < best_names)):
                    best_size = size
                    best_names = names
            return best_names

        # Increase threshold until we can peel off enough people.
        # Start near the first possible cut and use coarse-to-fine steps for speed.
        chosen_chunk_names = None
        jitteredGraph = _jitter_graph(groupGraph, epsilon=0.0001)
        base_cut_weight, _ = _best_min_cut(jitteredGraph)
        max_threshold = max(
            (sum(weight for weight in neighbors.values() if weight > 0) for neighbors in jitteredGraph.values()),
            default=0.0,
        ) + 1.0
        coarse_step = 0.01
        fine_step = 0.001
        coarse_start = max(0.0, base_cut_weight - coarse_step)

        first_valid_threshold = None
        threshold = coarse_start
        while threshold <= max_threshold + 1e-12:
            split = find_groups(jitteredGraph, ordered_group, weight_threshold=threshold)
            if len(split) > 1:
                candidate = pick_chunk(split)
                if candidate is not None:
                    first_valid_threshold = threshold
                    break
            threshold += coarse_step

        if first_valid_threshold is not None:
            threshold = max(coarse_start, first_valid_threshold - coarse_step)
            while threshold <= first_valid_threshold + 1e-12:
                split = find_groups(jitteredGraph, ordered_group, weight_threshold=threshold)
                if len(split) > 1:
                    chosen_chunk_names = pick_chunk(split)
                    if chosen_chunk_names is not None:
                        break
                threshold += fine_step

        if chosen_chunk_names is None:
            # Last chance: use the current min-cut weight directly as threshold.
            split = find_groups(jitteredGraph, ordered_group, weight_threshold=base_cut_weight + 1e-6)

            if len(split) > 1:
                chosen_chunk_names = pick_chunk(split)

        if chosen_chunk_names is None:
            raise RuntimeError(f"Could not split group: {[p.name for p in group]}")

        chosen_name_set = set(chosen_chunk_names)
        chosen_group = {person for person in group if person.name in chosen_name_set}
        remainder = {person for person in group if person.name not in chosen_name_set}

        newGroups.append(chosen_group)
        if remainder:
            pending.append(remainder)
            pending.sort(key=lambda group: tuple(sorted(person.name for person in group)))

    return newGroups
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


def _max_cut_threshold_upper_bound(graph):
    """Safe threshold cap for one group's min-cut sweep.

    For signed weights, a conservative upper bound is the largest positive
    weighted degree of any node.
    """
    max_positive_degree = 0.0
    for _, neighbors in graph.items():
        positive_degree = sum(weight for weight in neighbors.values() if weight > 0)
        if positive_degree > max_positive_degree:
            max_positive_degree = positive_degree
    return max_positive_degree + 1.0


def _chunk_quality(group_graph, kept_names, all_names):
    """Higher is better: cohesive kept chunk with weak positive ties to removed people."""
    removed_names = all_names - kept_names
    kept_sorted = sorted(kept_names)

    internal = 0.0
    for i in range(len(kept_sorted)):
        for j in range(i + 1, len(kept_sorted)):
            internal += group_graph.get(kept_sorted[i], {}).get(kept_sorted[j], 0.0)

    boundary_positive = 0.0
    for a in kept_names:
        for b in removed_names:
            w = group_graph.get(a, {}).get(b, 0.0)
            if w > 0:
                boundary_positive += w

    return internal - boundary_positive


def _best_chunk_from_split(split, group, max_group_size, required_leave, group_graph):
    all_names = {person.name for person in group}
    best_size = None
    best_quality = None
    best_names = None

    for subgroup in split:
        size = len(subgroup)
        if size == 0 or size > max_group_size:
            continue

        leave_count = len(group) - size
        if leave_count < required_leave:
            continue

        names = tuple(sorted(person.name for person in subgroup))
        quality = _chunk_quality(group_graph, set(names), all_names)

        is_better = False
        if best_size is None:
            is_better = True
        elif size > best_size:
            is_better = True
        elif size == best_size and quality > best_quality:
            is_better = True
        elif size == best_size and quality == best_quality and names < best_names:
            is_better = True

        if is_better:
            best_size = size
            best_quality = quality
            best_names = names

    if best_size is None:
        return None
    return best_size, best_quality, best_names


def _find_first_valid_chunk(jittered_graph, group, max_group_size, required_leave, group_graph):
    max_threshold = _max_cut_threshold_upper_bound(jittered_graph)

    # Coarse-to-fine threshold sweep to reduce expensive find_groups calls.
    coarse_step = 0.05
    medium_step = 0.005
    fine_step = 0.001

    def sweep(start, stop, step):
        t = start
        ordered_group = sorted(list(group), key=lambda person: person.name)
        while t <= stop + 1e-12:
            split = find_groups(jittered_graph, ordered_group, weight_threshold=t)
            if len(split) > 1:
                best = _best_chunk_from_split(split, group, max_group_size, required_leave, group_graph)
                if best is not None:
                    return t, best
            t += step
        return None, None

    coarse_t, coarse_best = sweep(0.0, max_threshold, coarse_step)
    if coarse_best is None:
        return None

    medium_start = max(0.0, coarse_t - coarse_step)
    medium_t, medium_best = sweep(medium_start, coarse_t, medium_step)
    if medium_best is None:
        return coarse_best

    fine_start = max(0.0, medium_t - medium_step)
    _, fine_best = sweep(fine_start, medium_t, fine_step)
    return fine_best or medium_best

def splitGroupsByMaxSize(graph, input, maxGroupSize):
    pending = find_groups(graph, input, weight_threshold=0)
    pending.sort(key=lambda group: tuple(sorted(person.name for person in group)))
    newGroups = []

    while pending:
        group = pending.pop(0)

        if len(group) <= maxGroupSize:
            newGroups.append(group)
            continue

        groupGraph = makeGraphFromInput(group)

        # Increase threshold until at least the overflow size can be cut off.
        # Example: 12 with table size 8 => need to cut at least 4.
        required_leave = len(group) - maxGroupSize
        chosen_chunk_names = None

        # Build one deterministic jittered graph once per group.
        jitteredGraph = _jitter_graph(groupGraph, epsilon=0.0001)
        best_chunk = _find_first_valid_chunk(jitteredGraph, group, maxGroupSize, required_leave, groupGraph)
        if best_chunk is not None:
            chosen_chunk_names = best_chunk[2]

        if chosen_chunk_names is None:
            # Last chance: use the current min-cut weight directly as threshold.
            cut_weight, _ = _best_min_cut(jitteredGraph)
            ordered_group = sorted(list(group), key=lambda person: person.name)
            split = find_groups(jitteredGraph, ordered_group, weight_threshold=cut_weight + 1e-6)

            if len(split) > 1:
                best_retry = _best_chunk_from_split(split, group, maxGroupSize, required_leave, groupGraph)
                if best_retry is not None:
                    chosen_chunk_names = best_retry[2]

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
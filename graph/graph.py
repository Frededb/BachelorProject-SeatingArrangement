import os
import sys
import heapq
from itertools import count

# Ensure project root on sys.path so imports work when module is imported/run
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

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

    pref_sets = {}
    avoid_sets = {}
    for name in names:
        person = name_to_person[name]

        prefs = set(getattr(person, "preferences", set()) or set())
        avoids = set(getattr(person, "avoidances", set()) or set())

        # Derive link sets from dynamic attributes when available.
        attributes = getattr(person, "attributes", []) or []
        attribute_set = getattr(person, "attribute_set", []) or []
        for idx, values in enumerate(attributes):
            if idx >= len(attribute_set) or not isinstance(values, list):
                continue
            meta = attribute_set[idx] if isinstance(attribute_set[idx], dict) else {}
            kind = str(meta.get("kind", "")).strip().lower()
            if kind not in {"prefence", "preference"}:
                continue

            try:
                weight = float(meta.get("weight", 0))
            except (TypeError, ValueError):
                weight = 0.0

            cleaned = {v for v in values if isinstance(v, str) and v}
            if weight < 0:
                avoids.update(cleaned)
            else:
                prefs.update(cleaned)

        pref_sets[name] = prefs
        avoid_sets[name] = avoids

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a_name = names[i]
            b_name = names[j]

            pref_count = int(b_name in pref_sets[a_name]) + int(a_name in pref_sets[b_name])
            avoid_count = int(b_name in avoid_sets[a_name]) + int(a_name in avoid_sets[b_name])
            weight = pref_count - avoid_count

            # Fully canceled pairs have no edge.
            if weight == 0:
                continue

            graph[a_name][b_name] = weight
            graph[b_name][a_name] = weight

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
    all_nodes = set(vertices)

    best_partition = (set(), set())
    best_cut = float('inf')

    while len(vertices) > 1:
        weights = {v: 0.0 for v in vertices}
        added = []
        added_set = set()
        for i in range(len(vertices)):
            sel = max((v for v in vertices if v not in added_set), key=lambda x: (weights[x], x))
            added.append(sel)
            added_set.add(sel)
            if i < len(vertices) - 1:
                for v in vertices:
                    if v not in added_set:
                        weights[v] += adj[sel].get(v, 0.0)
            else:
                t = sel
                s = added[-2]
                cut_weight = weights[t]

                S = set()
                for v in added[:-1]:
                    S |= v_sets[v]
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
            for nb, w in graph[node].items():
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
    person_by_name = {person.name: person for person in people}

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
    return [{person_by_name[name] for name in group if name in person_by_name} for group in groups]



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
    pending = []
    seq = count()
    person_by_name = {person.name: person for person in input}

    def _group_key(group):
        return tuple(sorted(person.name for person in group))

    # Fast initial split: avoid heavy work on the full graph when possible.
    components = find_connected_components(graph)
    for component in components:
        people_group = {person_by_name[name] for name in component if name in person_by_name}
        if people_group:
            heapq.heappush(pending, (_group_key(people_group), next(seq), people_group))

    if not pending and input:
        whole_group = set(input)
        heapq.heappush(pending, (_group_key(whole_group), next(seq), whole_group))

    newGroups = []

    while pending:
        _, _, group = heapq.heappop(pending)

        if len(group) <= maxGroupSize:
            newGroups.append(group)
            continue

        ordered_group = sorted(list(group), key=lambda person: person.name)
        groupGraph = makeGraphFromInput(ordered_group)

        # Density-weighted cohesion-based chunk selection
        chosen_chunk_names = _cohesion_chunk_names(groupGraph, maxGroupSize)
        if not chosen_chunk_names:
            # Fallback: if cohesion fails (e.g., extremely sparse/negative graph),
            # just take an arbitrary maxGroupSize subset by name to ensure progress.
            chosen_chunk_names = tuple(sorted(p.name for p in ordered_group[:maxGroupSize]))

        chosen_name_set = set(chosen_chunk_names)
        chosen_group = {person for person in group if person.name in chosen_name_set}
        remainder = {person for person in group if person.name not in chosen_name_set}

        newGroups.append(chosen_group)
        if remainder:
            heapq.heappush(pending, (_group_key(remainder), next(seq), remainder))

    return newGroups


def _cohesion_chunk_names(group_graph, chunk_size, alpha=2.0):
    """Select a cohesive chunk of up to chunk_size nodes using a density-weighted cohesion score.

    score(x, C) = (sum_{c in C} max(w(x,c), 0) - alpha * sum_{c in C} max(-w(x,c), 0)) / max(1, |C|)

    Returns a sorted tuple of chosen node names, or None if graph empty.
    """
    if not group_graph:
        return None

    names = sorted(group_graph.keys())
    target_size = min(chunk_size, len(names))

    # Precompute positive degree as a good seed heuristic
    def positive_degree(name):
        return sum(w for w in group_graph[name].values() if w > 0)

    # Seed: node with highest positive degree
    seed = max(names, key=lambda n: (positive_degree(n), n))
    chosen = {seed}

    while len(chosen) < target_size:
        best_name = None
        best_score = None
        for candidate in names:
            if candidate in chosen:
                continue
            pos_sum = 0.0
            neg_sum = 0.0
            for member in chosen:
                w = group_graph[candidate].get(member, 0.0)
                if w > 0:
                    pos_sum += w
                elif w < 0:
                    neg_sum += -w
            score = (pos_sum - alpha * neg_sum) / max(1, len(chosen))
            # Only accept candidates that do not decrease cohesion; require score > 0
            if score <= 0:
                continue
            key = (score, positive_degree(candidate), candidate)
            if best_score is None or key > best_score:
                best_score = key
                best_name = candidate

        if best_name is None:
            break
        chosen.add(best_name)

    # If for some reason only the seed was acceptable but target_size > 1,
    # we still return that single highly cohesive node.
    return tuple(sorted(chosen))

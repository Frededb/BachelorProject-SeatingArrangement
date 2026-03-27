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
        prefs = getattr(person, "preferences", set()) or set()
        avoids = getattr(person, "avoidances", set()) or set()
        pref_sets[name] = prefs if isinstance(prefs, set) else set(prefs)
        avoid_sets[name] = avoids if isinstance(avoids, set) else set(avoids)

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
    greedy_cutoff = max(maxGroupSize * 4, 32)

    def _group_key(group):
        return tuple(sorted(person.name for person in group))

    def _pick_greedy_chunk_names(group_graph, chunk_size):
        if not group_graph:
            return None

        target_size = min(chunk_size, len(group_graph))
        names = sorted(group_graph.keys())
        seed = max(
            names,
            key=lambda name: (sum(weight for weight in group_graph[name].values() if weight > 0), name),
        )
        chosen = {seed}

        while len(chosen) < target_size:
            best_name = None
            best_score = None
            for candidate in names:
                if candidate in chosen:
                    continue
                attach = sum(group_graph[candidate].get(member, 0.0) for member in chosen)
                positive_degree = sum(weight for weight in group_graph[candidate].values() if weight > 0)
                score = (attach, positive_degree, candidate)
                if best_score is None or score > best_score:
                    best_score = score
                    best_name = candidate

            if best_name is None:
                break
            chosen.add(best_name)

        return tuple(sorted(chosen))

    # Fast initial split: avoid global min-cut on the full graph when possible.
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
        group_size = len(ordered_group)
        required_leave = group_size - maxGroupSize

        if group_size >= greedy_cutoff:
            chosen_chunk_names = _pick_greedy_chunk_names(groupGraph, maxGroupSize)
        else:
            chosen_chunk_names = None

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
        base_cut_weight = None
        if chosen_chunk_names is None:
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
            split_cache = {}

            def get_split(threshold_value):
                cache_key = round(threshold_value, 6)
                if cache_key not in split_cache:
                    split_cache[cache_key] = find_groups(jitteredGraph, ordered_group, weight_threshold=threshold_value)
                return split_cache[cache_key]

            threshold = coarse_start
            while threshold <= max_threshold + 1e-12:
                split = get_split(threshold)
                if len(split) > 1:
                    candidate = pick_chunk(split)
                    if candidate is not None:
                        first_valid_threshold = threshold
                        break
                threshold += coarse_step

            if chosen_chunk_names is None and first_valid_threshold is not None:
                threshold = max(coarse_start, first_valid_threshold - coarse_step)
                while threshold <= first_valid_threshold + 1e-12:
                    split = get_split(threshold)
                    if len(split) > 1:
                        chosen_chunk_names = pick_chunk(split)
                        if chosen_chunk_names is not None:
                            break
                    threshold += fine_step

            if chosen_chunk_names is None and base_cut_weight is not None:
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
            heapq.heappush(pending, (_group_key(remainder), next(seq), remainder))

    return newGroups
import argparse
import math
import os
import sys
from collections import defaultdict

import gurobipy as gp
from gurobipy import GRB

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

UTILS_DIR = os.path.join(ROOT_DIR, "Utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from Utils import ValueCalc
from Utils.printer import printArrangementWithValues
from Utils.reader import emptyPerson, readjson

TABLE_SIZE = 8


def _directed_score(person_a, person_b) -> float:
    """Score contribution from A feeling about B (directed)."""
    if person_a.name == "Empty" or person_b.name == "Empty":
        return 0.0

    score = 0.0
    if person_a.studyprogram == person_b.studyprogram:
        score += 3.0
    if person_a.year == person_b.year:
        score += 1.0
    if person_b.name in person_a.preferences:
        score += 10.0
    if person_b.name in person_a.avoidances:
        score -= 10.0
    return score


def _pair_score_undirected(padded_people):
    """
    Build undirected pair scores:
      S_ij = score(i->j) + score(j->i)
    for i < j, skipping zeros.
    """
    n = len(padded_people)
    S = {}
    for i in range(n):
        for j in range(i + 1, n):
            sij = _directed_score(padded_people[i], padded_people[j])
            sji = _directed_score(padded_people[j], padded_people[i])
            s = sij + sji
            if s != 0.0:
                S[(i, j)] = s
    return S


def _seat_pair_weights_undirected(table_size=TABLE_SIZE):
    """
    Return weights for unordered seat pairs:
      W_pq = 1 / dist(p,q) for p < q
    """
    template = [None] * table_size
    W = {}
    for p in range(table_size):
        for q in range(p + 1, table_size):
            dist = ValueCalc.getDistanceTo(template, p, q)
            W[(p, q)] = 1.0 / float(dist)
    return W


def _avg_seat_pair_weight(W):
    """Average weight across unordered seat pairs (p<q)."""
    vals = list(W.values())
    return sum(vals) / max(1, len(vals))


def _set_common_params(model, time_limit, mip_gap, threads, verbose, focus="feasible"):
    model.Params.TimeLimit = float(time_limit)
    model.Params.MIPGap = float(mip_gap)
    if threads is not None:
        model.Params.Threads = int(threads)
    if not verbose:
        model.Params.OutputFlag = 0

    # Your objective is generally non-convex (negative edges), so be explicit.
    model.Params.NonConvex = 2

    # Focus on quickly finding strong solutions.
    # 1 = focus on finding feasible solutions quickly
    # 2 = focus on proving optimality
    model.Params.MIPFocus = 1 if focus == "feasible" else 2

    # Slightly more heuristics often helps on these problems.
    model.Params.Heuristics = 0.5


def _solve_table_assignment(
    padded_people,
    table_count,
    pair_scores_undirected,
    time_limit,
    mip_gap,
    threads,
    verbose,
):
    """
    Stage 1 (coarse): assign people to tables only (ignore exact seats).
    Objective uses average distance weight as a proxy.

    Variables:
      m[i,t] = 1 if person i is assigned to table t
    Constraints:
      sum_t m[i,t] = 1
      sum_i m[i,t] = 8  (with empties padded, always exact)
    Objective (proxy):
      maximize sum_t sum_{i<j} (S_ij * avgW) * m[i,t] * m[j,t]
    """
    n = len(padded_people)

    W = _seat_pair_weights_undirected(TABLE_SIZE)
    avgW = _avg_seat_pair_weight(W)

    model = gp.Model("seating_stage1_table_assignment")
    _set_common_params(
        model,
        time_limit=time_limit,
        mip_gap=mip_gap,
        threads=threads,
        verbose=verbose,
        focus="feasible",
    )

    m = model.addVars(n, table_count, vtype=GRB.BINARY, name="m")

    # Each person to exactly one table
    for i in range(n):
        model.addConstr(gp.quicksum(m[i, t] for t in range(table_count)) == 1, name=f"one_table_{i}")

    # Each table has exactly 8 people (empties included)
    for t in range(table_count):
        model.addConstr(gp.quicksum(m[i, t] for i in range(n)) == TABLE_SIZE, name=f"table_size_{t}")

    # Symmetry breaking: anchor person 0 to table 0
    if n > 0:
        model.addConstr(m[0, 0] == 1, name="anchor_person0_table0")

    # Quadratic proxy objective
    obj = gp.QuadExpr()
    for t in range(table_count):
        for (i, j), s in pair_scores_undirected.items():
            obj.add(s * avgW * m[i, t] * m[j, t])
    model.setObjective(obj, GRB.MAXIMIZE)
    model.optimize()

    if model.SolCount == 0:
        raise RuntimeError("Stage 1: Gurobi did not find a feasible table assignment.")

    # Extract groups per table (indices)
    tables = [[] for _ in range(table_count)]
    for i in range(n):
        for t in range(table_count):
            if m[i, t].X > 0.5:
                tables[t].append(i)
                break

    # Safety: enforce exact size
    for t in range(table_count):
        if len(tables[t]) != TABLE_SIZE:
            raise RuntimeError(f"Stage 1: Table {t} has {len(tables[t])} people, expected {TABLE_SIZE}.")

    return tables


def _solve_seats_for_one_table(
    table_indices,
    padded_people,
    pair_scores_undirected,
    W_undirected,
    time_limit,
    mip_gap,
    threads,
    verbose,
    table_id=0,
):
    """
    Stage 2 (fine): for a fixed set of 8 people, assign them to 8 seats.

    Variables:
      x[k,p] for k in 0..7 (people in this table) and p in 0..7 (seats)
    Constraints:
      each person exactly one seat
      each seat exactly one person
    Objective:
      maximize sum_{i<j} S_ij * sum_{p<q} W_pq * (x_i_p x_j_q + x_i_q x_j_p)
    """
    # Map local k -> global person index
    local_to_global = list(table_indices)
    K = TABLE_SIZE

    # Pre-filter pairs that exist within this table
    local_pairs = []
    for a in range(K):
        ga = local_to_global[a]
        for b in range(a + 1, K):
            gb = local_to_global[b]
            s = pair_scores_undirected.get((min(ga, gb), max(ga, gb)), 0.0)
            if s != 0.0:
                local_pairs.append((a, b, s))

    model = gp.Model(f"seating_stage2_table{table_id}_seats")
    _set_common_params(
        model,
        time_limit=time_limit,
        mip_gap=mip_gap,
        threads=threads,
        verbose=verbose,
        focus="feasible",
    )

    x = model.addVars(K, TABLE_SIZE, vtype=GRB.BINARY, name="x")

    for a in range(K):
        model.addConstr(gp.quicksum(x[a, p] for p in range(TABLE_SIZE)) == 1, name=f"one_seat_person_{a}")

    for p in range(TABLE_SIZE):
        model.addConstr(gp.quicksum(x[a, p] for a in range(K)) == 1, name=f"one_person_seat_{p}")

    # Symmetry breaking inside a table:
    # Fix the smallest global index person to seat 0. (Keeps tables comparable & reduces symmetric seat permutations.)
    anchor_local = min(range(K), key=lambda k: local_to_global[k])
    model.addConstr(x[anchor_local, 0] == 1, name="anchor_min_person_seat0")

    obj = gp.QuadExpr()
    # Only unordered seat pairs (p<q), and add both seat-orderings via (x_i_p x_j_q + x_i_q x_j_p)
    for (p, q), w in W_undirected.items():
        for a, b, s in local_pairs:
            obj.add(s * w * (x[a, p] * x[b, q] + x[a, q] * x[b, p]))

    model.setObjective(obj, GRB.MAXIMIZE)
    model.optimize()

    if model.SolCount == 0:
        raise RuntimeError(f"Stage 2: No feasible seat assignment found for table {table_id}.")

    # Extract seat order as global person indices
    seat_to_global = [None] * TABLE_SIZE
    for p in range(TABLE_SIZE):
        for a in range(K):
            if x[a, p].X > 0.5:
                seat_to_global[p] = local_to_global[a]
                break

    return seat_to_global, model.ObjVal, model.Status


def optimize_seating(people, time_limit=60, mip_gap=0.01, threads=None, verbose=True):
    """
    Improved approach (much faster in practice):
      Stage 1: assign people -> tables (coarse MIQP, no seat dimension)
      Stage 2: for each table, assign people -> seats (tiny MIQP per table)

    This avoids the huge monolithic MIQP with (people × tables × seats) variables AND (seat pairs × people pairs × tables)
    terms in a single solve.
    """
    table_count = math.ceil(len(people) / TABLE_SIZE)
    seat_count = table_count * TABLE_SIZE
    padded_people = list(people) + [emptyPerson] * (seat_count - len(people))
    n = len(padded_people)

    pair_scores_undirected = _pair_score_undirected(padded_people)
    W_undirected = _seat_pair_weights_undirected(TABLE_SIZE)

    # Time split: most time to stage 1, remainder to stage 2 across tables.
    time_limit = float(time_limit)
    stage1_time = max(5.0, time_limit * 0.65)
    stage2_total = max(1.0, time_limit - stage1_time)
    per_table_time = max(0.5, stage2_total / max(1, table_count))

    # Stage 1: tables
    table_groups = _solve_table_assignment(
        padded_people=padded_people,
        table_count=table_count,
        pair_scores_undirected=pair_scores_undirected,
        time_limit=stage1_time,
        mip_gap=mip_gap,
        threads=threads,
        verbose=verbose,
    )

    # Stage 2: seats per table
    arrangement = [[emptyPerson] * TABLE_SIZE for _ in range(table_count)]
    table_objvals = []
    table_statuses = []

    for t in range(table_count):
        seat_to_global, objval, status = _solve_seats_for_one_table(
            table_indices=table_groups[t],
            padded_people=padded_people,
            pair_scores_undirected=pair_scores_undirected,
            W_undirected=W_undirected,
            time_limit=per_table_time,
            mip_gap=mip_gap,
            threads=threads,
            verbose=verbose,
            table_id=t,
        )
        table_objvals.append(objval)
        table_statuses.append(status)

        for s in range(TABLE_SIZE):
            arrangement[t][s] = padded_people[seat_to_global[s]]

    print("=== Gurobi results ===")
    print(f"People: {len(people)} (padded to {n}), tables: {table_count}, seats: {seat_count}")
    print(f"Time split: stage1={stage1_time:.1f}s, stage2 per table={per_table_time:.2f}s")
    print(f"Stage2 table objectives (sum): {sum(table_objvals):.4f}")
    printArrangementWithValues(arrangement)

    return arrangement


def main():
    parser = argparse.ArgumentParser(description="Optimize seating arrangement with Gurobi (fast 2-stage MIQP).")
    parser.add_argument(
        "--input",
        default=os.path.join(ROOT_DIR, "Inputs", "input100People.json"),
        help="Path to input json file.",
    )
    parser.add_argument("--time-limit", type=float, default=60.0, help="Total time limit in seconds.")
    parser.add_argument("--mip-gap", type=float, default=0.01, help="Target MIP gap for each stage.")
    parser.add_argument("--threads", type=int, default=None, help="Optional thread count.")
    parser.add_argument("--quiet", action="store_true", help="Disable Gurobi solver output.")
    args = parser.parse_args()

    people = readjson(args.input)
    optimize_seating(
        people,
        time_limit=args.time_limit,
        mip_gap=args.mip_gap,
        threads=args.threads,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
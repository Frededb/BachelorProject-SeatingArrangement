import argparse
import math
import os
import sys

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


def base_pair_score(person_a, person_b):
	if person_a.name == "Empty" or person_b.name == "Empty":
		return 0.0

	score = 0.0
	if person_a.studyprogram == person_b.studyprogram:
		score += 3.0 * 2
	if person_a.year == person_b.year:
		score += 1.0 * 2
	if person_b.name in person_a.preferences:
		score += 10.0
	if person_b.name in person_a.avoidances:
		score -= 10.0
	if person_a.name in person_b.preferences:
		score += 10.0
	if person_a.name in person_b.avoidances:
		score -= 10.0
	return score


def distance_weights(table_size=TABLE_SIZE):
	table_template = [None] * table_size
	weights = {}
	for seat_a in range(table_size):
		for seat_b in range(seat_a + 1, table_size):
			dist = ValueCalc.getDistanceTo(table_template, seat_a, seat_b)
			weights[(seat_a, seat_b)] = 1.0 / dist
	return weights


def optimize_seating(people, time_limit=60, mip_gap=0.01, threads=None, verbose=True):
	table_count = math.ceil(len(people) / TABLE_SIZE)
	seat_count = table_count * TABLE_SIZE
	padded_people = list(people) + [emptyPerson] * (seat_count - len(people))
	person_count = len(padded_people)

	pair_scores = {}
	for i in range(person_count):
		for j in range(i + 1, person_count):
			combined_score = base_pair_score(padded_people[j], padded_people[i])
			if combined_score != 0:
				pair_scores[(i, j)] = combined_score

	model = gp.Model("seating_miqp")
	model.Params.TimeLimit = time_limit
	model.Params.MIPGap = mip_gap
	if threads is not None:
		model.Params.Threads = threads
	if not verbose:
		model.Params.OutputFlag = 0

	x = model.addVars(person_count, table_count, TABLE_SIZE, vtype=GRB.BINARY, name="x")

	for i in range(person_count):
		model.addConstr(
			gp.quicksum(x[i, t, s] for t in range(table_count) for s in range(TABLE_SIZE)) == 1,
			name=f"assign_person_{i}",
		)

	for t in range(table_count):
		for s in range(TABLE_SIZE):
			model.addConstr(
				gp.quicksum(x[i, t, s] for i in range(person_count)) == 1,
				name=f"fill_seat_t{t}_s{s}",
			)

	seat_weights = distance_weights(TABLE_SIZE)
	objective = gp.QuadExpr()
	for t in range(table_count):
		for (i, j), pair_score in pair_scores.items():
			for (seat_a, seat_b), seat_weight in seat_weights.items():
				nudge = math.sqrt(j*seat_a + i*seat_b) * 1e-6
				coeff = pair_score * seat_weight + nudge
				objective += coeff * x[i, t, seat_a] * x[j, t, seat_b]
				objective += coeff * x[i, t, seat_b] * x[j, t, seat_a]

	model.setObjective(objective, GRB.MAXIMIZE)
	model.optimize()

	if model.SolCount == 0:
		raise RuntimeError("Gurobi did not find a feasible seating arrangement.")

	arrangement = [[emptyPerson] * TABLE_SIZE for _ in range(table_count)]
	for t in range(table_count):
		for s in range(TABLE_SIZE):
			for i in range(person_count):
				if x[i, t, s].X > 0.5:
					arrangement[t][s] = padded_people[i]
					break

	print(f"Gurobi status: {model.Status}")
	print(f"Gurobi objective: {model.ObjVal:.4f}")
	if model.Status in (GRB.OPTIMAL, GRB.TIME_LIMIT, GRB.SUBOPTIMAL, GRB.INTERRUPTED):
		print(f"Best bound: {model.ObjBound:.4f}")
		if math.isfinite(model.MIPGap):
			print(f"Gap: {model.MIPGap:.4%}")

	printArrangementWithValues(arrangement)
	return arrangement


def main():
	parser = argparse.ArgumentParser(description="Optimize seating arrangement with Gurobi (MIQP).")
	parser.add_argument(
		"--input",
		default=os.path.join(ROOT_DIR, "Inputs", "input100People.json"),
		help="Path to input json file.",
	)
	parser.add_argument("--time-limit", type=float, default=60.0, help="Gurobi time limit in seconds.")
	parser.add_argument("--mip-gap", type=float, default=0.01, help="Target MIP gap.")
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

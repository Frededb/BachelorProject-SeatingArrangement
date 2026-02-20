import gurobipy as gp
from gurobipy import GRB
import math
import sys
import os

# Add parent directory to path to allow importing from Utils
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
# Add Utils directory to path so internal imports in Utils (like 'import reader') work
sys.path.append(os.path.join(parent_dir, 'Utils'))

from Utils.Person import Person
from Utils.printer import printArrangementWithValues
from Utils.reader import emptyPerson

def get_distance(seat_index_1, seat_index_2, table_width):
    """
    Calculates distance between two seat indices based on table width.
    Rows are determined by index // width. Columns by index % width.
    """
    # Coordinates for seat 1
    r1 = seat_index_1 // table_width
    c1 = seat_index_1 % table_width
    
    # Coordinates for seat 2
    r2 = seat_index_2 // table_width
    c2 = seat_index_2 % table_width
    
    dist = math.sqrt((r1 - r2)**2 + (c1 - c2)**2)
    return dist

def calculate_relationship_score(p1, p2):
    """
    Calculates the compatibility score between two people based on:
    - Same study program: +3
    - Same year: +1
    - Preferences: +10
    - Avoidances: -10
    """
    if p1 == p2:
        return 0
        
    score = 0
    if p1.studyprogram == p2.studyprogram:
        score += 3
    if p1.year == p2.year:
        score += 1
    if p2.name in p1.preferences:
        score += 10
    if p2.name in p1.avoidances:
        score -= 10
        
    return score

def optimize_arrangement(people, table_capacity, num_tables):
    try:
        num_people = len(people)
        total_seats = table_capacity * num_tables
        table_width = table_capacity // 2 

        if num_people > total_seats:
            raise ValueError(f"Not enough seats! People: {num_people}, Seats: {total_seats}")

        m = gp.Model("multi_table_seating")
        m.Params.TimeLimit = 180 # Set a time limit (seconds) because 100 people is hard
        m.Params.MIPFocus = 1   # Focus on finding feasible solutions quickly
        m.Params.LogToConsole = 1

        # --- Variables ---
        # x[p, t, s] = 1 if person p is at table t in seat s
        x = m.addVars(num_people, num_tables, table_capacity, vtype=GRB.BINARY, name="x")

        # --- Constraints ---

        # 1. Each person assigned to exactly one table/seat
        m.addConstrs(
            (gp.quicksum(x[p, t, s] for t in range(num_tables) for s in range(table_capacity)) == 1 
             for p in range(num_people)), 
            name="person_assigned"
        )

        # 2. Each seat has at most one person
        m.addConstrs(
            (gp.quicksum(x[p, t, s] for p in range(num_people)) <= 1 
             for t in range(num_tables) for s in range(table_capacity)), 
            name="seat_capacity"
        )

        # --- Objective ---
        obj = gp.QuadExpr()

        # Precompute distances for a single table reference
        distances = {}
        for s1 in range(table_capacity):
            for s2 in range(table_capacity):
                if s1 != s2:
                    distances[(s1, s2)] = get_distance(s1, s2, table_width)

        # Build Objective
        # We only care about relationships between p1 and p2 if they are at the SAME table
        
        # Optimization: Only consider pairs with non-zero relationship scores
        significant_pairs = []
        for i in range(num_people):
            for j in range(i + 1, num_people): # Avoid duplicates (i,j) and (j,i)
                score = calculate_relationship_score(people[i], people[j])
                if score != 0:
                    significant_pairs.append((i, j, score))
        
        print(f"Optimizing {len(significant_pairs)} significant relationships...")

        for (p1_idx, p2_idx, score) in significant_pairs:
            # For each table, if both are at this table at specific seats, add score
            for t in range(num_tables):
                for s1 in range(table_capacity):
                    for s2 in range(table_capacity):
                        if s1 == s2: continue
                        
                        dist = distances[(s1, s2)]
                        term_value = score * (1.0 / dist)
                        
                        # Add term: score * (1/dist) * x[p1,t,s1] * x[p2,t,s2]
                        # Since graph is undirected, we add for both directions or multiply by 2 if symmetric logic
                        obj.addTerms(term_value, x[p1_idx, t, s1], x[p2_idx, t, s2])
                        obj.addTerms(term_value, x[p1_idx, t, s2], x[p2_idx, t, s1])

        m.setObjective(obj, GRB.MAXIMIZE)

        m.optimize()

        # --- Output ---
        if m.SolCount > 0:
            print(f"\nSolution Found! Total Objective Value from Gurobi: {m.objVal}")
            arrangement = []
            
            for t in range(num_tables):
                table_seats = [emptyPerson] * table_capacity # Initialize with emptyPerson for unassigned seats
                for s in range(table_capacity):
                    for p in range(num_people):
                        if x[p, t, s].X > 0.5:
                            table_seats[s] = people[p]
                
                arrangement.append(table_seats)
            
            printArrangementWithValues(arrangement)
            return arrangement
        else:
            print("No solution found.")
            return None

    except gp.GurobiError as e:
        print(f'Error code {e.errno}: {e}')
    except AttributeError:
        print('Encountered an attribute error')

import json

if __name__ == "__main__":
    # Load data from input100People.json
    try:
        with open("../Inputs/input100People.json", "r") as f:
            people_data = json.load(f)
            
        people_list = []
        for p_data in people_data:
            person = Person(
                name=p_data["name"],
                studyprogram=p_data["studyprogram"],
                year=p_data["year"],
                preferences=p_data.get("preferences"),
                avoidances=p_data.get("avoidances")
            )
            people_list.append(person)

        print(f"Loaded {len(people_list)} people.")

        # Test with a subset of people (e.g. 24) across 3 tables
        subset_size = 24
        # subset_size = len(people_list) # Uncomment to run for all 100 people (will take longer)
        
        subset_people = people_list[:subset_size] 
        capacity_per_table = 8
        num_tables = (len(subset_people) + capacity_per_table - 1) // capacity_per_table
        
        print(f"Optimizing {len(subset_people)} people into {num_tables} tables of {capacity_per_table}...")
        optimize_arrangement(subset_people, capacity_per_table, num_tables)
        
    except FileNotFoundError:
        print("Error: input100People.json not found in ../Inputs/")
    except Exception as e:
        print(f"An error occurred: {e}")

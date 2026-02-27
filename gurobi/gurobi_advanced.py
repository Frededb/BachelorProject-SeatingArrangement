import gurobipy as gp
from gurobipy import GRB

try:
    # --- 1. Data Preparation ---
    # Commodities (Keys) and their profits (Values)
    commodities = ['Pencils', 'Pens', 'Erasers', 'Mugs']
    profits = {
        'Pencils': 10,
        'Pens': 20,
        'Erasers': 5,
        'Mugs': 30
    }

    # Resources (Keys) and their total capacities (Values)
    resources = ['Metal', 'Plastic', 'Rubber', 'Time']
    capacities = {
        'Metal': 100,
        'Plastic': 150,
        'Rubber': 40,
        'Time': 60
    }

    # Resource consumption for each commodity (Matrix-like data)
    # Format: (commodity, resource): amount_required
    requirements = {
        ('Pencils', 'Metal'): 1, ('Pencils', 'Plastic'): 0, ('Pencils', 'Rubber'): 2, ('Pencils', 'Time'): 1,
        ('Pens', 'Metal'): 2,    ('Pens', 'Plastic'): 1,    ('Pens', 'Rubber'): 0,    ('Pens', 'Time'): 2,
        ('Erasers', 'Metal'): 0, ('Erasers', 'Plastic'): 0, ('Erasers', 'Rubber'): 3, ('Erasers', 'Time'): 1,
        ('Mugs', 'Metal'): 5,    ('Mugs', 'Plastic'): 10,   ('Mugs', 'Rubber'): 0,    ('Mugs', 'Time'): 5
    }

    # --- 2. Model Initialization ---
    m = gp.Model("production_planning")

    # --- 3. Variables ---
    # addVars creates a "TupleDict" of variables indexed by the list 'commodities'.
    # name="production" gives variables names like production[Pencils], production[Pens], etc.
    # vtype=GRB.INTEGER means we can only make whole items.
    production = m.addVars(commodities, vtype=GRB.INTEGER, name="production")

    # --- 4. Objective Function ---
    # Maximize total profit: sum(production[c] * profit[c] for c in commodities)
    # production.prod(profits) is a helper for dot products (sum of variable * coefficient)
    m.setObjective(production.prod(profits), GRB.MAXIMIZE)

    # --- 5. Constraints ---
    # We add one constraint for each resource type 'r'.
    # The constraint ensures: sum(requirements[c, r] * production[c] for c in commodities) <= capacity[r]
    
    # Using generator expression with quicksum (efficient summation)
    # m.addConstrs is a bulk generator for constraints
    m.addConstrs(
        (gp.quicksum(requirements[c, r] * production[c] for c in commodities) <= capacities[r]
         for r in resources),
        name="Resource_Limit"
    )

    # --- 6. Parameters (Optional tuning) ---
    m.Params.TimeLimit = 10  # Stop after 10 seconds
    m.Params.MIPGap = 0.05   # Stop when within 5% of optimal

    # --- 7. Optimize ---
    m.write("production_planning.lp") # Useful for debugging: writes the math model to a file
    m.optimize()

    # --- 8. Results ---
    if m.status == GRB.OPTIMAL:
        print("\n--- Optimal Solution Found ---")
        print(f"Total Profit: ${m.ObjVal}")
        print("\nProduction Plan:")
        for c in commodities:
            # retrieve variable value using the key
            count = production[c].X 
            if count > 0:
                print(f"  Produce {int(count)} {c}")
        
        # Checking Slack (unused capacity)
        print("\nResource Usage:")
        for r in resources:
            constr = m.getConstrByName(f"Resource_Limit[{r}]")
            print(f"  {r}: {constr.RHS - constr.Slack} consumed out of {constr.RHS}")

    else:
        print("Optimal solution was not found.")

except gp.GurobiError as e:
    print(f'Error code {e.errno}: {e}')
except AttributeError:
    print('Encountered an attribute error')

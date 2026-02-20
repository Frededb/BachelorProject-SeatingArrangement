import gurobipy as gp
from gurobipy import GRB

try:
    # Create a new model
    model = gp.Model("mip1")

    # Create variables
    x = model.addVar(vtype=GRB.BINARY, name="x")
    y = model.addVar(vtype=GRB.BINARY, name="y")
    z = model.addVar(vtype=GRB.BINARY, name="z")

    # Set objective: maximize x + y + 2z
    model.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

    # Add constraints
    # c0: x + 2y + 3z <= 4
    model.addConstr(x + 2 * y + 3 * z <= 4, "c0")
    
    # c1: x + y >= 1
    model.addConstr(x + y >= 1, "c1")

    # Optimize model
    model.optimize()

    # Print solution
    for v in model.getVars():
        print(f'{v.varName} {v.x}')

    print(f'Obj: {model.objVal}')

except gp.GurobiError as e:
    print(f'Error code {e.errno}: {e}')

except AttributeError:
    print('Encountered an attribute error')
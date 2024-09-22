from pyomo import environ as pe

# Define the model
model = pe.ConcreteModel()

# Define the decision variables
model.x = pe.Var(initialize=0.0, within=pe.NonNegativeReals)
model.y = pe.Var(initialize=0.0, within=pe.NonNegativeReals)
model.z = pe.Var(initialize=0.0, within=pe.NonNegativeReals)

# Define a parameter
model.P = pe.Param(default=5.0, mutable=True)

# Define the objective function (maximize the sum of x, y, and z)
model.obj = pe.Objective(expr=model.x + model.y + model.z, sense=pe.maximize)

# Define the constraints
model.c1 = pe.Constraint(expr=model.x + model.y * model.P <= 10)
model.c2 = pe.Constraint(expr=model.x + model.z <= 20.0)
model.c3 = pe.Constraint(expr=model.y + model.z * model.P <= 10.0)

# Solve the model using the GLPK solver
solver = pe.SolverFactory('glpk')
solver.solve(model)

# Print the results
print(f"x = {model.x.value}, y = {model.y.value}, z = {model.z.value}")

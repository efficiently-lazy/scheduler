from pyomo import environ as pe

model = pe.ConcreteModel()
model.x = pe.Var(initialize=1.0)
model.y = pe.Var(initialize=1.0)
model.z = pe.Var(initialize=1.0)

model.obj = pe.Objective(expr=model.x + model.y + model.z)

model.c1 = pe.Constraint(expr=model.x + model.y >= 1.0)
model.c2 = pe.Constraint(expr=model.x + model.z >= 1.0)

model.c3 = pe.Constraint(expr=model.y + model.z >= 1.0)

solver = pe.SolverFactory('glpk')
solver.solve(model)

print(model.x.value, model.y.value, model.z.value)
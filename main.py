from pyomo import environ as pyo
import random
import numpy as np


if __name__ == "__main__":
    # Define the model
    model = pyo.ConcreteModel()

    # Define the sets
    model.P = pyo.RangeSet(1, 5)
    model.D = pyo.RangeSet(1, 3)
    model.M = pyo.RangeSet(1, 10)
    model.T = pyo.RangeSet(1, 20)

    # Define the parameters
    O_values = {}
    for i in range(1, 6):
        for j in range(1, 11):
            O_values[i, j] = random.randint(0, 1)
    
    
    B_values = {}
    for i in range(1, 4):
        for j in range(1, 11):
            B_values[i, j] = random.randint(0, 1)
    
    model.O = pyo.Param(
        model.P, model.M,
        default=0,
        mutable=False,
        initialize=O_values,
        doc="Product ownership matrix between set product P and set managers M"
        )
    
    model.B = pyo.Param(
        model.D, model.M,
        default=0,
        mutable=False,
        initialize=B_values,
        doc="Binary matrix representing the relation between developer D and manager M"
        )

    # Define the decision variables
    model.ProductReviewed = pyo.Var(
        model.P, model.T,
        initialize=0.0,
        within=pyo.Binary
        )
    model.ScheduleReview = pyo.Var(
        model.D, model.M, model.P, model.T,
        initialize=0.0,
        within=pyo.Binary
        )

    # Define the objective function to maximize the sum of y variables
    model.obj = pyo.Objective(expr=pyo.summation(model.ProductReviewed), sense=pyo.maximize)

    # Define the constraints
    def product_max_once_reviewed(model, p):
        return sum(
            model.ProductReviewed[p, t]
            for t in model.T) <= 1
    
    def product_manager_restriction(model, p, m):
        return sum(
            model.ScheduleReview[d, m, p, t]
            for d in model.D
            for t in model.T) <= model.O[p, m]
    
    def manager_developer_restriction(model, m, d):
        return sum(
            model.ScheduleReview[d, m, p, t]
            for p in model.P
            for t in model.T) <= model.B[d, m] * len(model.P)

    def linking_variable_constraints(model, p, t):
        return sum(
            model.ScheduleReview[d, m, p, t]
            for d in model.D
            for m in model.M) <= model.ProductReviewed[p, t]
    
    def developer_max_once_review(model, d, t):
        return sum(
            model.ScheduleReview[d, m, p, t]
            for m in model.M
            for p in model.P) <= 1


    def manager_max_once_review(model, m, t):
        return sum(
            model.ScheduleReview[d, m, p, t]
            for d in model.D
            for p in model.P) <= 1

    model.c1 = pyo.Constraint(model.P,
                              rule=product_max_once_reviewed)
    model.c2 = pyo.Constraint(model.P, model.M,
                              rule=product_manager_restriction)
    model.c3 = pyo.Constraint(model.M, model.D,
                              rule=manager_developer_restriction)
    model.c4 = pyo.Constraint(model.P, model.T,
                              rule=linking_variable_constraints)
    model.c5 = pyo.Constraint(model.D, model.T,
                              rule=developer_max_once_review)
    model.c6 = pyo.Constraint(model.M, model.T,
                              rule=manager_max_once_review)


    # Solve the model using the GLPK solver
    solver = pyo.SolverFactory('glpk')
    # Create a model instance and optimize
    instance = model.create_instance()
    results = solver.solve(instance)

    # Print the results
    print(model.obj())

    for v in instance.component_objects(pyo.Var, active=True):
        for index in v:
            if pyo.value(v[index]) != 0:
                print("Variable",v)  
                print ("   ",index, pyo.value(v[index]))  

    # for parmobject in instance.component_objects(pyo.Param, active=True):
    #     nametoprint = str(str(parmobject.name))
    #     print ("Parameter ", nametoprint)  
    #     for index in parmobject:
    #         vtoprint = pyo.value(parmobject[index])
    #         print ("   ",index, vtoprint)  
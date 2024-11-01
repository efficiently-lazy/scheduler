from pyomo import environ as pyo
import random
import pandas as pd
import numpy as np

from utils.input_init import init__set, init_params, init_variables
import utils.constraints as const

def initialize_scheduler(product_ownership: pd.DataFrame,
                         work_relations: pd.DataFrame,
                         availability: pd.DataFrame) -> pyo.ConcreteModel:
    """ Initialize the optimization model based on the input dataframes.
    
    Args:
        product_ownership (pd.DataFrame): product ownership matrix of managers
        work_relations (pd.DataFrame): matrix describing work relations between developers and managers
        availability (pd.DataFrame): availability dataframeof managers and developers

    Returns:
        pyo.ConcreteModel: Pyomo model
    """
    # Define the model
    model = pyo.ConcreteModel()
    init__set(model, product_ownership, work_relations, availability)
    init_params(model, product_ownership, work_relations, availability)
    init_variables(model)

    return model

def initialize_objective(model: pyo.ConcreteModel) -> None:
    model.obj = pyo.Objective(
        expr=pyo.summation(model.ProductReviewed),
        sense=pyo.maximize
        )

def add_constraints(model: pyo.ConcreteModel):    
    model.c1 = pyo.Constraint(model.Products,
                                rule=const.product_max_once_reviewed)
    model.c2 = pyo.Constraint(model.Products, model.Managers,
                                rule=const.product_manager_restriction)
    model.c3 = pyo.Constraint(model.Managers, model.Developers,
                                rule=const.manager_developer_restriction)
    model.c4 = pyo.Constraint(model.Products, model.Time,
                                rule=const.linking_variable_constraints)
    model.c5 = pyo.Constraint(model.Developers, model.Time,
                                rule=const.developer_max_once_review)
    model.c6 = pyo.Constraint(model.Managers, model.Time,
                                rule=const.manager_max_once_review)

def print_results(instance: pyo.ConcreteModel):
    for v in instance.component_objects(pyo.Var, active=True):
        for index in v:
            if pyo.value(v[index]) != 0:
                print("Variable",v)  
                print ("   ",index, pyo.value(v[index]))  

import pandas as pd
from pyomo import environ as pyo

def init__set(model: pyo.ConcreteModel,
              product_ownership: pd.DataFrame,
              work_relations: pd.DataFrame,
              availability: pd.DataFrame) -> None:
    """ Initialize Sets for the optimization model.

    Args:
        model (pyo.ConcreteModel): Pyomo model
        product_ownership (pd.DataFrame): product ownership matrix of managers
        work_relations (pd.DataFrame): matrix describing work relations between developers and managers
        availability (pd.DataFrame): availability dataframeof managers and developers
    """
    model.Products = pyo.Set(initialize=list(product_ownership.index))
    model.Developers = pyo.Set(initialize=list(work_relations.index))
    model.Managers = pyo.Set(initialize=list(product_ownership.columns))
    model.Time = pyo.Set(initialize=list(availability.index))

def init_params(model: pyo.ConcreteModel,
                product_ownership: pd.DataFrame,
                work_relations: pd.DataFrame,
                availability: pd.DataFrame) -> None:
    """ Initialize parameters for the optimization model.

    Args:
        model (pyo.ConcreteModel): Pyomo model
        product_ownership (pd.DataFrame): product ownership matrix of managers
        work_relations (pd.DataFrame): matrix describing work relations between developers and managers
        availability (pd.DataFrame): availability dataframeof managers and developers
    """
    model.OwnershipProduct = pyo.Param(
        model.Products,
        model.Managers,
        initialize={
            (p, m): product_ownership.loc[p,m]
            for p, m in model.Products * model.Managers
        })
    model.WorkRelations = pyo.Param(
        model.Developers,
        model.Managers,
        initialize={
            (d, m): work_relations.loc[d,m]
            for d, m in model.Developers * model.Managers
        })
    model.Availability = pyo.Param(
        model.Time * model.Managers | model.Time * model.Developers,
        initialize={
            (t, i): availability.loc[t, i] 
            for t in model.Time
            for i in model.Managers | model.Developers
        })

def init_variables(model: pyo.ConcreteModel) -> None:
    """ Initialize variables for the optimization model.

    Args:
        model (pyo.ConcreteModel): Pyomo model
    """
    model.ProductReviewed = pyo.Var(model.Products, model.Time,
                                    within=pyo.Binary)
    model.ScheduleReview = pyo.Var(model.Developers, model.Managers, model.Products, model.Time,
                                   within=pyo.Binary)

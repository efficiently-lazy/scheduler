from pyomo import environ as pyo
import pandas as pd

def print_results(instance: pyo.ConcreteModel):
    for v in instance.component_objects(pyo.Var, active=True):
        for index in v:
            if pyo.value(v[index]) != 0:
                print("Variable",v)  
                print ("   ",index, pyo.value(v[index]))  

def create_result_schedule(instance: pyo.ConcreteModel,
                           dict_availability: dict[pd.DataFrame]
                           ) -> dict:
    """ Create a dataframe based on the availability matrix plus
    the newly assigned schedule for each developer and manager
    with the to-be-reviewed products.

    Args:
        instance (pyo.ConcreteModel): Pyomo result instance
        dict_availability (dict[pd.DataFrame]): 

    Returns:
        dict: dict of newly assigned availability matrix
    """
    result = dict_availability.copy()
    for (d, m, p, t) in instance.ScheduleReview:
        if pyo.value(instance.ScheduleReview[d, m, p, t]) != 0:
            [sheet, time] = t.split(" || ")
            df = result[sheet]
            df.loc[time, d] = p
            df.loc[time, m] = p

    return result
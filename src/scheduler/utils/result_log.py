from pyomo import environ as pyo
import pandas as pd

def print_results(instance: pyo.ConcreteModel):
    print("\nOptimization results:")
    reviewed_products = []

    for index in instance.ProductReviewed:
        value = pyo.value(instance.ProductReviewed[index])
        if value != 0:
            reviewed_products.append(index[0])

    print(f"Number of reviewed products: {len(reviewed_products)}")

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
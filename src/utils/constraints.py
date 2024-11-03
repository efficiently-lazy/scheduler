import pandas as pd
from pyomo import environ as pyo


def product_max_once_reviewed(model, p):
    """ Only one product can be reviewed one at a time."""
    return sum(
        model.ProductReviewed[p, t]
        for t in model.Time) <= 1

def product_manager_restriction(model, p, m):
    """ Only one product can be reviewed by one product manager and
    the product must be owned by the manager.
    """
    return sum(
        model.ScheduleReview[d, m, p, t]
        for d in model.Developers
        for t in model.Time) <= model.OwnershipProduct[p, m]

def manager_developer_restriction(model, m, d):
    """ Developer must only work with the manager that belongs to the
    same team as him/her. 
    """
    return sum(
        model.ScheduleReview[d, m, p, t]
        for p in model.Products
        for t in model.Time) <= model.WorkRelations[d, m] * len(model.Products)

def linking_variable_constraints(model, p, t):
    """ Linking constraints between ScheduleReview and ProductReviewed.
    If product is deemed to be reviewed by ScheduleReview, it means
    ProductReviewed needs to be set to 1.
    """
    return sum(
        model.ScheduleReview[d, m, p, t]
        for d in model.Developers
        for m in model.Managers) == model.ProductReviewed[p, t]

def developer_max_once_review(model, d, t):
    """ Only one developer can review one product at a time. """
    return sum(
        model.ScheduleReview[d, m, p, t]
        for m in model.Managers
        for p in model.Products) <= 1

def manager_max_once_review(model, m, t):
    """ Only one manager can review one product at a time. """
    return sum(
        model.ScheduleReview[d, m, p, t]
        for d in model.Developers
        for p in model.Products) <= 1

def schedules_not_blocked(model, m, d, p, t):
    """ Schedules of participating developer and manager should not be blocked
     during the assigned product review appointments. """
    return (
        2 * model.ScheduleReview[d, m, p, t]  <= 
        (2 - model.Availability[t, d] - model.Availability[t, m]))

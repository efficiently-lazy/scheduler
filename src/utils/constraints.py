import pandas as pd
from pyomo import environ as pyo


def product_max_once_reviewed(model, p):
    return sum(
        model.ProductReviewed[p, t]
        for t in model.Time) <= 1

def product_manager_restriction(model, p, m):
    return sum(
        model.ScheduleReview[d, m, p, t]
        for d in model.Developers
        for t in model.Time) <= model.OwnershipProduct[p, m]

def manager_developer_restriction(model, m, d):
    return sum(
        model.ScheduleReview[d, m, p, t]
        for p in model.Products
        for t in model.Time) <= model.WorkRelations[d, m] * len(model.Products)

def linking_variable_constraints(model, p, t):
    return sum(
        model.ScheduleReview[d, m, p, t]
        for d in model.Developers
        for m in model.Managers) == model.ProductReviewed[p, t]

def developer_max_once_review(model, d, t):
    return sum(
        model.ScheduleReview[d, m, p, t]
        for m in model.Managers
        for p in model.Products) <= 1

def manager_max_once_review(model, m, t):
    return sum(
        model.ScheduleReview[d, m, p, t]
        for d in model.Developers
        for p in model.Products) <= 1
from pyomo import environ as pyo
import pandas as pd
from utils.io_handler import load_input_data, write_output_data
import bin.model as m

def schedule_meetings(input_file: str, output_path: str):
    # Load data
    product_ownership, work_relations, availability = load_input_data(input_file)
    
    # Create model and initialize the parameters, sets, and variables
    model = m.initialize_scheduler(product_ownership, work_relations, availability)

    # Set objective function for the model to maximize number of reviewed products
    m.initialize_objective(model)

    # Add constraints to the model
    m.add_constraints(model)
    

    # Solve the model using the GLPK solver
    solver = pyo.SolverFactory('glpk')
    instance = model.create_instance()
    results = solver.solve(instance)

    # Print results
    m.print_results(instance)

    # Write results in an excel file
    result = m.create_result_schedule(instance, availability)
    write_output_data(result, output_path)
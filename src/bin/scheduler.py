from pyomo import environ as pyo
import pandas as pd

from utils.io_handler import load_input_data, load_availability,write_output_data
from utils.result_log import print_results, create_result_schedule

import bin.model as m

def schedule_meetings(input_file: str, availability_file: str, output_path: str):
    # Load data
    product_ownership, work_relations = load_input_data(input_file)
    availability, dict_availability = load_availability(availability_file)
    
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

    # Print results for quick inspection
    # m.print_results(instance)

    # Write results in an excel file
    result = create_result_schedule(instance, dict_availability)
    write_output_data(result, output_path)

    print('Scheduler finished!')
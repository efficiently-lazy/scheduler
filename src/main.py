from pyomo import environ as pyo
import pandas as pd

from scheduler.utils.io_handler import load_input_data, load_availability,write_output_data
from scheduler.utils.result_log import print_results, create_result_schedule

import scheduler.model as m

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
    result_solver = solver.solve(model)
    print(f"\nSolver status: {result_solver.solver.status} and termination status: {result_solver.solver.termination_condition}")

    # Print results for quick inspection
    print_results(model)

    # Write results in an excel file
    result = create_result_schedule(model, dict_availability)
    write_output_data(result, output_path)

    print('\nScheduler finished!')

if __name__ == '__main__':
    print('Scheduler starting...\n')
    input_file = 'src/data/input.xlsx'
    availability_file = 'src/data/availability.xlsx'
    output_path = 'src/data/output.xlsx'

    schedule_meetings(input_file, availability_file, output_path)


from pyomo.environ import SolverFactory
import pandas as pd
from utils.io_handler import load_input_data, write_output_data
from bin.model import create_scheduling_model

def schedule_meetings(input_file, output_file):
    # Load data
    products, availability = load_input_data(input_file)
    
    # Prepare data for model
    product_dict = {row['ProductID']: row for _, row in products.iterrows()}
    team_availability = {row['Timeslot']: row['Available'] for _, row in availability.iterrows()}
    
    # Create model
    model = create_scheduling_model(product_dict, team_availability)
    
    # Solve model
    solver = SolverFactory('glpk')
    solver.solve(model)
    
    # Process results
    schedule = []
    for p in model.products:
        for t in model.timeslots:
            if model.schedule[p, t].value == 1:
                schedule.append({
                    'ProductID': p,
                    'Timeslot': t,
                    'Scheduled': 'Yes'
                })
                
    schedule_df = pd.DataFrame(schedule)
    write_output_data(schedule_df, output_file)

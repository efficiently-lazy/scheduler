import pandas as pd

def load_input_data(input_file):
    product_data = pd.read_excel(input_file, sheet_name='Products')
    availability_data = pd.read_excel(input_file, sheet_name='Availability')
    return product_data, availability_data

def write_output_data(schedule, output_file):
    with pd.ExcelWriter(output_file) as writer:
        schedule.to_excel(writer, sheet_name='Meetings', index=False)

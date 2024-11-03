import pandas as pd
import numpy as np

pd.set_option("future.no_silent_downcasting", True)

def load_input_data(input_file) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Load data from an excel input file and returns three dataframes for
    product ownership matrix, work relations matrix and availability matrix.

    Args:
        input_file (str): path to the input file

    Returns:
        tuple: product_ownership, work_relations, availability as dataframes
    """
    product_ownership = pd.read_excel(input_file, sheet_name='Ownership Products', index_col=0)
    work_relations = pd.read_excel(input_file, sheet_name='Work Relation', index_col=0)
    availability = pd.read_excel(input_file, sheet_name='Availability', index_col=0)

    # Convert x into 1 and NaN into 0
    product_ownership = product_ownership.replace('x', 1).fillna(0)
    work_relations = work_relations.replace('x', 1).fillna(0)

    return product_ownership, work_relations, availability

def write_output_data(schedule, output_file):
    with pd.ExcelWriter(output_file) as writer:
        schedule.to_excel(writer, sheet_name='Meetings', index=False)

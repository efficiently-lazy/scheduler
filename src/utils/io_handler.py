import pandas as pd
import numpy as np

pd.set_option("future.no_silent_downcasting", True)

def load_input_data(input_file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """ Load data from an excel input file and returns two dataframes for
    product ownership matrix and work relations matrix.

    Args:
        input_file (str): path to the input file

    Returns:
        tuple: product_ownership and work_relations as dataframes
    """
    try:
        product_ownership = pd.read_excel(input_file, sheet_name='Ownership Products', index_col=0)
        work_relations = pd.read_excel(input_file, sheet_name='Work Relation', index_col=0)

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file {input_file} not found.")

    except ValueError as e:
        raise ValueError(f"Error reading sheets: {e}")

    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")

    # Convert 'x' into 1 and NaN into 0
    product_ownership = product_ownership.replace('x', 1).fillna(0)
    work_relations = work_relations.replace('x', 1).fillna(0)

    return product_ownership, work_relations

def load_availability(availability_file) -> pd.DataFrame:
    """ Load availability data from an excel file with sheet name 
    as date and index as the time. Returning a dataframe with index 
    of the concantenated date and time of the matrix, and dict of the 
    availability matrix per day.

    Args:
        availability_file (str): path to the availability file

    Returns:
        pd.DataFrame: availability as a dataframe
        dict: dictionary of availability per day
    """
    if not availability_file:
        raise ValueError("Availability file path cannot be empty")

    consolidated_availability = pd.DataFrame(index=[], columns=[])
    dict_availability = {}
    try:
        # Iterating through the sheets and creating availability dataframes
        list_sheets = pd.ExcelFile(availability_file).sheet_names
        for sheet in list_sheets:
            availability_original = pd.read_excel(availability_file, sheet_name=sheet, index_col=0, dtype=str)
            availability = availability_original.replace('x', 1).fillna(0)
            availability.index = [sheet + ' || ' + str(idx) for idx in availability.index]
            
            # Allocation of availability dataframes
            dict_availability[sheet] = availability_original
            consolidated_availability = pd.concat([consolidated_availability, availability])
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File {availability_file} cannot be found.")
    
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"File {availability_file} is empty.")
    
    except pd.errors.ParserError:
        raise pd.errors.ParserError(f"File {availability_file} is not a valid Excel file.")

    return consolidated_availability, dict_availability

def write_output_data(schedule: dict[pd.DataFrame], output_file: str):
    """
    Write the meeting schedule to an Excel file.

    Args:
        schedule (dict[pd.DataFrame]): A dictionary of meeting schedules for each day.
        output_file (str): The path to the output Excel file.

    Returns:
        None
    """
    if schedule is None:
        raise ValueError("Schedule cannot be None")

    if not output_file:
        raise ValueError("Output file path cannot be empty")

    try:
        with pd.ExcelWriter(output_file) as writer:
            for sheet, df in schedule.items():
                df.to_excel(writer, sheet_name=sheet)            
    except FileNotFoundError:
        raise FileNotFoundError(f"File {output_file} cannot be found.")
    
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"File {output_file} is empty.")

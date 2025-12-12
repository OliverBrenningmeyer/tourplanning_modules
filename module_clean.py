import pandas as pd
import os
from datetime import datetime
import ast
from module_column_mapping import get_column_mapping, EXPECTED_COLUMNS
from module_client_configuration import CONFIG
import math


def normalize_column_names(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """
    Normalize column names based on a provided mapping.
    Any columns not in the mapping will remain unchanged.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_mapping (dict): A dictionary mapping raw column names to normalized names.

    Returns:
        pd.DataFrame: DataFrame with normalized column names.
    """
    return df.rename(columns=column_mapping)

# Update the ensure_columns_exist function to use EXPECTED_COLUMNS
def ensure_columns_exist(df: pd.DataFrame, EXPECTED_COLUMNS) -> pd.DataFrame:
    """
    Ensure that all expected columns exist in the DataFrame.
    If a column is missing, it will be created and filled with NaN.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with all expected columns.
    """
    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            df[column] = None  # Create empty columns with None values
    return df

def ensure_column_as_string(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Ensure the specified column is treated as a string.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to convert to string.

    Returns:
        pd.DataFrame: DataFrame with the specified column as string.
    """
    df[column_name] = df[column_name].astype(str)
    return df

def ensure_column_as_integer(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Ensure the specified column is treated as an integer without decimals.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to convert to integer.

    Returns:
        pd.DataFrame: DataFrame with the specified column as integer.
    """
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0).apply(lambda x: int(x))
    return df

# Update the function signature to include `client_name`
def clean_and_process_data(df: pd.DataFrame, base_date_str: str, output_folder_path: int, client_name: str) -> pd.DataFrame:
    """
    Perform advanced cleaning and processing steps on the DataFrame:
    - Normalize column names
    - Filter non-null 'customer_branch_cluster' and set some to 'non'
    - Ensure 'customer_Lieferschein' is treated as a string
    - Replace German umlauts
    - Replace null values with extreme values in time columns
    - Convert times to ISO format
    - Modify zero or missing weight values
    - Create integer capacity values
    - Filter by weight limit
    - Filter by date

    Returns cleaned and processed DataFrame.
    """

    """
    #Activate the following code if you want to use the functions to normalize column names
    #and ensure all expected columns exist.
    """
    # Retrieve column mapping for the client
    column_mapping = get_column_mapping(client_name)

    # Normalize column names
    df = normalize_column_names(df, column_mapping)

    # Ensure all expected columns exist
    df = ensure_columns_exist(df,EXPECTED_COLUMNS)

    # Retrieve the client configuration
    client_config_order = CONFIG[client_name]["order"]
    timewindows = client_config_order.get('timewindow', True)  # Use the value from client_config_order, default to True if not provided

    
    # Function to filter non-null 'customer_branch_cluster'
    # Assuming 'customer_branch_cluster' is the column to be filtered
    # and it should not be null, empty, or 'NaN'
    def filter_non_null_customer_branch_cluster(df):
        return df[df['customer_branch_cluster'].apply(lambda x: pd.notnull(x) and x != '' and x != 'NaN')]

    # Function to set 'customer_dispobereich' to 'non' if 'Auftr.-Nr.' has a value
    def set_notdefined_dispobereich_to_non(df):
        df.loc[df['Auftr.-Nr.'].notnull(), 'customer_branch_cluster'] = 'non'
        return df

    # Function to replace German umlauts with their respective replacements
    # Assuming 'ä' -> 'ae', 'ö' -> 'oe', 'ü' -> 'ue'
    # and 'ß' -> 'ss'
    def replace_umlauts(text):
        if isinstance(text, str):
            return text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        return text

    # Function to replace null values with extreme values
    # Assuming 'Entl. von  (Auftr.)' and 'Entl. bis (Auftr.)' are the columns to be replaced
    # and they are in the format 'dd.mm.yy HH:MM'
    # Replace null values with the minimum and maximum values of the respective columns
    # and return the modified DataFrame
    def replace_null_with_extreme_values(df, column_min, column_max):
        if column_min not in df.columns or column_max not in df.columns:
            raise KeyError(f"Required columns '{column_min}' or '{column_max}' are missing.")
        min_value = df[column_min].min()
        max_value = df[column_max].max()
        df.loc[:, column_min] = df[column_min].fillna(min_value)
        df.loc[:, column_max] = df[column_max].fillna(max_value)
        return df

    # Function to convert time columns to ISO format
    # - If 'Entl. bis (Auftr.)' has a time of 00:00, it will be changed to 18:00 in 'Termin bis ISO'.
    # - If `timewindows` is True:
    #   - Convert 'Entl. von  (Auftr.)' and 'Entl. bis (Auftr.)' to datetime using the format 'dd.mm.yy %H:%M'.
    #   - Create 'Termin von ISO' and 'Termin bis ISO' columns in ISO 8601 format.
    # - If `timewindows` is False:
    #   - Only convert 'Entl. bis (Auftr.)' to datetime and create 'Termin bis ISO' in ISO 8601 format for 6 PM
    # - Create a new column 'day' from the date part of 'Entl. bis (Auftr.)'.
    def convert_to_iso(df, timewindows: bool):
        # Ensure 'Entl. bis (Auftr.)' is converted to datetime before using .dt accessor
        df['Entl. bis (Auftr.)'] = pd.to_datetime(df['Entl. bis (Auftr.)'], errors='coerce')

        # Now safely use the .dt accessor and set times if 00:00 to 23:59 for the end of the timewindow
        df.loc[df['Entl. bis (Auftr.)'].dt.time == datetime.strptime('00:00', '%H:%M').time(), 'Termin bis ISO'] = \
            df['Entl. bis (Auftr.)'].dt.strftime('%Y-%m-%dT18:00:00Z')
        
        if timewindows:
            df.loc[:, 'Entl. von  (Auftr.)'] = pd.to_datetime(df['Entl. von  (Auftr.)'], format='%d.%m.%y %H:%M')
            df.loc[:, 'Entl. bis (Auftr.)'] = pd.to_datetime(df['Entl. bis (Auftr.)'], format='%d.%m.%y %H:%M')
            df.loc[:, 'Termin von ISO'] = df['Entl. von  (Auftr.)'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            df.loc[:, 'Termin bis ISO'] = df['Entl. bis (Auftr.)'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            df.loc[:, 'Entl. bis (Auftr.)'] = pd.to_datetime(df['Entl. bis (Auftr.)'], format='%d.%m.%y %H:%M')
            df.loc[:, 'Termin bis ISO'] = df['Entl. bis (Auftr.)'].dt.strftime('%Y-%m-%dT18:00:00Z')

        df.loc[:, 'day'] = df['Entl. bis (Auftr.)'].dt.date
        return df

    # Function to filter DataFrame by date
    # Assuming 'day' is the column to be filtered
    # and base_date_str is in 'YYYY-MM-DD' format
    # Convert base_date_str to datetime.date object
    # and filter the DataFrame
    # to include only rows where 'day' matches base_date
    def filter_by_date(df, base_date_str):
        base_date = datetime.strptime(base_date_str, "%Y-%m-%d").date()
        return df[df['day'] == base_date]

    # Function to modify zero or missing weight values
    # Assuming 'customer_shipment_weight_kg' is the column to be modified
    # Replace 0 or NaN with 1
    def modify_zero_weight(df):
        df.loc[:, 'customer_shipment_weight_kg'] = df['customer_shipment_weight_kg'].replace(0, 1).fillna(1)
        return df

    # Function to create integer capacity values
    # Assuming 'customer_shipment_volume_units' is a float and needs to be converted to int
    def create_int_capacity(df):
        df['customer_shipment_volume_units'] = pd.to_numeric(df['customer_shipment_volume_units'], errors='coerce')
        # Replace NaN and inf with 0 before converting to int
        df['customer_shipment_volume_units'] = df['customer_shipment_volume_units'].fillna(0)
        return df
    
    # Function to adjust 'customer_shipment_volume_units' based on the configuration:
    def adjust_volume_units_for_client(df, client_config):
        # - If client_config["order"]["volume_unit_size"] is set and > 0, divide each value by this size,
        #   round up to the next integer, and store as int.
        #   Example: volume_unit_size=50, value=120 → 120/50=2.4 → math.ceil=3
        # - Regardless of whether the division/rounding was performed, multiply each value by 10 and convert to int.
        #   Example: 3 * 10 = 30
        # - This standardizes the volume units for further processing.
        volume_unit_size = client_config.get("order", {}).get("volume_unit_size", None)
        if volume_unit_size is not None and volume_unit_size > 0:
            df['customer_shipment_volume_units'] = pd.to_numeric(df['customer_shipment_volume_units'], errors='coerce').fillna(0)
            df['customer_shipment_volume_units'] = df['customer_shipment_volume_units'].apply(
                lambda x: int(math.ceil(x / volume_unit_size)) if x > 0 else 0
            )
        df.loc[:, 'customer_shipment_volume_units'] = (df['customer_shipment_volume_units'] * 10).astype(int)

        return df

    def filter_weight_below_weightlimit(df, weight_limit):
        # Convert the column to numeric, errors='coerce' will replace invalid values with NaN
        df['customer_shipment_weight_kg'] = pd.to_numeric(df['customer_shipment_weight_kg'], errors='coerce')
        # Now filter based on weight limit
        return df[df['customer_shipment_weight_kg'] <= weight_limit]
    
    # Function to extract first word from 'customer_branch_cluster' and save it back
    def extract_first_word_and_save(df):
        df.loc[:, 'customer_branch_cluster'] = df['customer_branch_cluster'].apply(lambda x: x.split()[0] if isinstance(x, str) else x)

    # Function to replace umlauts in 'customer_branch_cluster'
    def replace_umlauts_in_column(df):
        df.loc[:, 'customer_branch_cluster'] = df['customer_branch_cluster'].apply(replace_umlauts)

    # Function to create a new folder to store the results in the defined path
    def create_new_folder(base_date_str,output_folder_path):
        os.makedirs(output_folder_path, exist_ok=True)
        print(f'Folder created at {output_folder_path}')

    # Function to fill empty cells in a column with a defined value
    def fill_empty_cells(df, column_name, fill_value):
        """
        Fill empty cells in the specified column with a defined value.

        Args:
            df (pd.DataFrame): The input DataFrame.
            column_name (str): The name of the column to fill.
            fill_value: The value to fill empty cells with.

        Returns:
            pd.DataFrame: DataFrame with empty cells in the column filled.
        """
        if column_name not in df.columns:
            raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")
        df[column_name] = df[column_name].fillna(fill_value)
        return df
    
    def fill_columns_with_defaults_and_handle_menge(df, client_config):
        """
        Fill columns with default values (overridable by config) and handle 'customer_menge' logic.
        """
        # Define defaults
        default_values = {
            'customer_telefonnummer': 'n/a',
            'customer_name': 'n/a',
            'customer_lange_cm': '1',
            'customer_breite_cm': '1',
            'customer_hohe_cm': '1',
            'customer_menge': '1',
            'customer_einheit': 'Piece'
        }

        # Override defaults with config values if present
        client_order_config = client_config.get("order", {})
        for col, default in default_values.items():
            value = client_order_config.get(col, default)
            df = fill_empty_cells(df, col, value)

        # Handle 'customer_menge' type conversion based on config
        if client_order_config.get('customer_menge', False):
            # Use customer_shipment_volume_units as values for customer_menge
            df['customer_menge'] = df['customer_shipment_volume_units']/10  # Use standardized volume units
            df = ensure_column_as_integer(df, 'customer_menge')
            df = ensure_column_as_string(df, 'customer_menge')
        else:
            df = ensure_column_as_integer(df, 'customer_menge')
            df = ensure_column_as_string(df, 'customer_menge')

        return df

    def handle_lieferschein_column(df, client_config):
        lieferschein_config = client_config.get("customer_Lieferschein", {"default": True})
        if not lieferschein_config.get("default", True):
            alt_col = lieferschein_config.get("alternativeDataColumn")
            if alt_col in df.columns:
                df["customer_Lieferschein"] = df[alt_col]
        return df

    # Process data
    client_config = CONFIG[client_name]

    create_new_folder(base_date_str,output_folder_path)
    df['Auftr.-Nr.'] = df['Auftr.-Nr.'].astype(str) # To add a prefix, use this: 'TO' + df['Auftr.-Nr.'].astype(str)

    df = handle_lieferschein_column(df, client_config)
    df = ensure_column_as_string(df, 'customer_Lieferschein')     # Ensure 'customer_Lieferschein' is treated as a string

    df = filter_non_null_customer_branch_cluster(df)
    extract_first_word_and_save(df)
    replace_umlauts_in_column(df)
    df = modify_zero_weight(df)
    df = replace_null_with_extreme_values(df, 'Entl. von  (Auftr.)', 'Entl. bis (Auftr.)')
    df = convert_to_iso(df, timewindows)
    df = create_int_capacity(df)
    adjust_volume_units_for_client(df, client_config)

    # Call the new function for filling columns and handling 'customer_menge'
    df = fill_columns_with_defaults_and_handle_menge(df, client_config)

    #df = filter_weight_below_weightlimit(df, weight_limit) # Uncomment this line if you want to filter by weight limit and then also add the weight limit parameter to the function
    df = filter_by_date(df, base_date_str)

    return df
import pandas as pd
import numpy as np
from datetime import time
import networkx as nx
from io import BytesIO
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates


def merge_results(vrp_response_json: dict, df_geocoded: pd.DataFrame, output_folder_path: str, depots_path: str) -> None:
    # Funktion zum Laden des DataFrames aus Excel
    def load_dataframe(file_path):
        return pd.read_excel(file_path, engine='openpyxl')

    depots = load_dataframe(depots_path)
    print(f"Depots DataFrame loaded with {len(depots)} rows.")
    
    """
    Merges the VRP response JSON with the geocoded DataFrame and saves the result to a CSV file.
    
    Parameters:
    - vrp_response_json (dict): The JSON response from the VRP API.
    - df_geocoded (pd.DataFrame): The DataFrame containing geocoded data.
    
    Returns:
    - merged_df with a full join of the VRP response and geocoded DataFrame on jobId = Auftr.-Nr.
    - df_unassigned_jobs: A list of dictionaries containing unassigned job details.

    """
    def idenify_unassigned_jobs(vrp_response_json):
        """
        Identify unassigned jobs from the VRP response JSON.
        
        Parameters:
        - vrp_response_json (dict): The JSON response from the VRP API.
        
        Returns:
        - unassigned_jobs_data (list): A list of dictionaries containing unassigned job details.
        """
        unassigned_jobs = []
        for job in vrp_response_json.get("unassigned", []):
            job_id = job["jobId"]
            reasons = "; ".join([f"{reason['code']}: {reason['description']}" for reason in job["reasons"]])
            unassigned_jobs.append({
                "Vehicle ID": "Unassigned",
                "Job ID": job_id,
                "Reasons": reasons
            })
        return unassigned_jobs

    # Step 1: Extract all activities from all tours
    all_activities = []
    for tour in vrp_response_json['tours']:
        vehicle_id = tour["vehicleId"]
        type_id = tour["typeId"]
        
        for stop in tour['stops']:
            for activity in stop['activities']:
                depot = type_id.split("-")[0]
                all_activities.append({
                            "Vehicle ID": vehicle_id,
                            "Type ID": type_id,
                            "Job ID": activity["jobId"],
                            "Activity Type": activity["type"],
                            "Latitude": activity["location"]["lat"],
                            "Longitude": activity["location"]["lng"],
                            "Start Time": activity["time"]["start"],
                            "End Time": activity["time"]["end"],
                            "Distance": stop["distance"]
                })

    # Step 2: Create a DataFrame from the extracted activities
    activities_df = pd.DataFrame(all_activities)

    # Step 3: Perform the left join with df_geocoded
    merged_df = pd.merge(activities_df, df_geocoded, left_on='Job ID', right_on='Auftr.-Nr.', how='left')
    
    # Step 4: Add conditional columns based on the activity type and normalize to 'here' for pickup, delivery and others
    def add_columns_and_normalize(row):
        if row['Activity Type'] == 'pickup': #pickup, as stated in the json response from the vrp
            # Normalize to 'here'
            row['here_lat'] = row['pickup_lat']
            row['here_lng'] = row['pickup_lng']
            row['here_id'] = row['pickup_id']
            row['here_input'] = row['pickup_input']
            row['here_label'] = row['pickup_label']
            row['here_countryCode'] = row['pickup_countryCode']
            row['here_city'] = row['pickup_city']
            row['here_street'] = row['pickup_street']
            row['here_postalCode'] = row['pickup_postalCode']
            row['here_houseNumber'] = row['pickup_houseNumber']
            row['here_queryScore'] = row['pickup_queryScore']
        elif row['Activity Type'] == 'delivery': #delivery, as stated in the json response from the vrp
            row['here_lat'] = row['dropoff_lat']
            row['here_lng'] = row['dropoff_lng']
            row['here_id'] = row['dropoff_id']
            row['here_input'] = row['dropoff_input']
            row['here_label'] = row['dropoff_label']
            row['here_countryCode'] = row['dropoff_countryCode']
            row['here_city'] = row['dropoff_city']
            row['here_street'] = row['dropoff_street']
            row['here_postalCode'] = row['dropoff_postalCode']
            row['here_houseNumber'] = row['dropoff_houseNumber']
            row['here_queryScore'] = row['dropoff_queryScore']
        else:
            # If not pickup or dropoff, set here columns to NaN
            row['here_lat'] = None
            row['here_lng'] = None
            row['here_id'] = None
            row['here_input'] = None
            row['here_label'] = None
            row['here_countryCode'] = None
            row['here_city'] = None
            row['here_street'] = None
            row['here_postalCode'] = None
            row['here_houseNumber'] = None
            row['here_queryScore'] = None
        return row

    # Apply the function to add conditional columns and normalize
    merged_df = merged_df.apply(add_columns_and_normalize, axis=1)

    def fill_here_pickup_with_depot_from_df(row):
        if row['Activity Type'] == 'pickup' and depots is not None:
            cluster = row.get('customer_dispobereich') or row.get('customer_branch_cluster')
            if cluster:
                depot_row = depots[depots['Dispobereich'].astype(str).str.strip().str.lower() == str(cluster).strip().lower()]
                if not depot_row.empty:
                    depot_row = depot_row.iloc[0]
                    for col in ['here_id','here_input','here_label','here_countryCode','here_city','here_street','here_postalCode','here_houseNumber','here_queryScore']:
                        if pd.isna(row.get(col)) or row.get(col) == '' or row.get(col) == 'n/a':
                            row[col] = depot_row.get(col, row.get(col))
                    # 'Vers.-Name' immer mit Bel.-StO. Kürzel aus Depot
                    row['Vers.-Name'] = depot_row.get('Bel.-StO. Kürzel', row.get('Vers.-Name'))
        return row

    merged_df = merged_df.apply(fill_here_pickup_with_depot_from_df, axis=1)
    
    # Step 5: Modify merged_df based on the Activity Types
    def modify_columns_based_on_activity_type(row):
        if row['Activity Type'] == 'delivery':
            # Ensure we handle None or NaN values for strings directly
            fahrerhinweis = row.get('Fahrerhinweis (Auftr.)', '')
            anm_lieferzeit = row.get('Anm. Lieferzeit', '')

            # Replace NaN with empty strings explicitly
            fahrerhinweis = '' if pd.isna(fahrerhinweis) else fahrerhinweis
            anm_lieferzeit = '' if pd.isna(anm_lieferzeit) else anm_lieferzeit

            # Combine the values, ensuring no trailing semicolons
            row['customer_Lieferhinweis'] = f"{fahrerhinweis}; {anm_lieferzeit}".strip('; ').strip()
            row['customer_Lieferschein'] = row.get('customer_Lieferschein', 'n/a')
            # Set other columns based on the delivery activity type
            row['customer_telefonnummer'] = row.get('customer_telefonnummer', 'n/a') #if empty, set to n/a, because it requirest a value
            row['customer_name'] = 'n/a' if pd.isna(row.get('customer_name')) else row.get('customer_name')  #if empty or nan, set to n/a, because it requirest a value
            row['here_company_name'] = row.get('Empfänger', 'n/a')  #if empty, set to n/a, because it requirest a value
        elif row['Activity Type'] == 'pickup':
            # For pickup activity types, set specific columns to None
            row['customer_Lieferhinweis'] = None
            row['customer_Lieferschein'] = row.get('customer_Lieferschein', 'n/a')
            row['customer_telefonnummer'] = 'n/a' #because it requirest a value
            row['customer_name'] = 'n/a' #because it requirest a value
            # Set here_company_name to the value from 'Vers.-Name' or 'n/a' if not available
            row['here_company_name'] = row.get('Vers.-Name', 'n/a') #if empty, set to n/a, because it requirest a value
        else:
            row['customer_Lieferhinweis'] = None
            row['customer_Lieferschein'] = row.get('customer_Lieferschein', 'n/a')
            row['customer_telefonnummer'] = 'n/a' #because it requirest a value
            row['customer_name'] = 'n/a' #because it requirest a value
            row['here_company_name'] = None
        return row

    # Apply the function to modify columns based on the activity type
    merged_df = merged_df.apply(modify_columns_based_on_activity_type, axis=1)

    # Step 6: Identify unassigned jobs fro the VRP response JSON
    df_unassigned_jobs = idenify_unassigned_jobs(vrp_response_json)

    # Ensure the function returns the correct types
    if not isinstance(merged_df, pd.DataFrame):
        raise TypeError("Expected merged_df to be a pandas DataFrame")

    return merged_df, df_unassigned_jobs



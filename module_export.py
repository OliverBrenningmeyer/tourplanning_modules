import pandas as pd

def create_bexos_import_csv(merged_df: pd.DataFrame) -> None:
    """
    Create a CSV file for BEXOS import from the merged DataFrame.
    
    Parameters:
    - merged_df (pd.DataFrame): The DataFrame containing merged data.

    - export_columns (dict): A dictionary mapping original column names to new names for export.
    
    Returns:
    - export_df: to be saved as a CSV file with the relevant columns for BEXOS import.
    """

    # Step 1: Define the columns to be included in the export and their corresponding export names
    export_columns = {
        "Vehicle ID": "Vehicle ID",
        "Type ID": "Type ID",
        "Job ID": "Job ID",
        "Activity Type": "Activity Type",
        "Latitude": "Latitude",
        "Longitude": "Longitude",
        "Start Time": "Start Time",
        "End Time": "End Time",
        "Distance": "Distance",

        "customer_shipment_volume_units": "customer_space_PAL",
        "customer_shipment_weight_kg": "customer_menge_kg",
        "customer_Lieferhinweis": "customer_Lieferhinweis",
        "customer_Lieferschein": "customer_pickup_reference",
        "customer_menge": "customer_menge",

        "here_id": "here_id",
        "here_input": "here_input",
        "here_label": "here_label",
        "here_countryCode": "here_countryCode",
        "here_city": "here_citys",
        "here_street": "here_street",
        "here_postalCode": "here_postalCode",
        "here_houseNumber": "here_houseNumber",
        "here_queryScore": "here_queryScore",

        "here_company_name": "here_company_name",
        "customer_branch_cluster": "customer_dispobereich",
        
        "customer_beschreibung": "customer_beschreibung",
        "customer_lange_cm": "customer_lange_cm",
        "customer_breite_cm": "customer_breite_cm",
        "customer_hohe_cm": "customer_hohe_cm",
        "customer_einheit": "customer_einheit",
        "customer_telefonnummer": "customer_telefonnummer",
        "customer_name": "customer_name"
    }

    # Step 2: Filter and rename the columns for export
    export_df = merged_df[list(export_columns.keys())].rename(columns=export_columns)

    return export_df
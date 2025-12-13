# module_column_mapping.py

# Define a central list of expected columns
EXPECTED_COLUMNS = [
    "customer_branch_cluster",
    "Entl. von  (Auftr.)",
    "Entl. bis (Auftr.)",
    "customer_Lieferschein",
    "Auftr.-Nr.",
    "Entladeart",
    "customer_shipment_weight_kg",
    "customer_shipment_volume_units",
    "Fahrerhinweis (Auftr.)",
    "Anm. Lieferzeit",
    "Vers.-Str.",
    "Vers.-Str.-Nr.",
    "Vers.-PLZ",
    "Vers.-Name",
    "Vers.-Ort",
    "Empfänger",
    "Empf.-PLZ",
    "Empf.-Ort",
    "Empf.-Str.",
    "Empf.-Str.-Nr.",
    "customer_lange_cm",
    "customer_breite_cm",
    "customer_hohe_cm",
    "customer_einheit",
    "customer_telefonnummer",
    "customer_name",
    "customer_beschreibung",
    "customer_menge"
]

# Example column mappings for different clients
# The CLIENT_COLUMN_MAPPINGS dictionary maps raw column names (specific to each client)
# to standardized column names used throughout the processing pipeline.
# This ensures that the code can handle client-specific data formats while maintaining
# a consistent internal structure.
# Column names, not part of the mapping, will not be changed.

CLIENT_COLUMN_MAPPINGS = {
    "Stark": {
        "Entl. von  (Auftr.)":"Entl. von  (Auftr.)",
        "Entl. bis (Auftr.)":"Entl. bis (Auftr.)",
        "customer_Lieferschein":"customer_Lieferschein",
        "Auftr.-Nr.":"Auftr.-Nr.",
        "Entladeart":"Entladeart",
        "Gewicht_[kg]":"customer_shipment_weight_kg", # Mapped key to new internal processing name
        "Volumen_[Stellplatz]":"customer_shipment_volume_units", # Mapped key to new internal processing name
        "Fahrerhinweis (Auftr.)":"Fahrerhinweis (Auftr.)",
        "Anm. Lieferzeit":"Anm. Lieferzeit",
        "Vers.-Str.":"Vers.-Str.",
        "Vers.-Str.-Nr.":"Vers.-Str.-Nr.",
        "Vers.-PLZ":"Vers.-PLZ",
        "Vers.-Name":"Vers.-Name",
        "Vers.-Ort":"Vers.-Ort",
        "Empfänger":"Empfänger",
        "Empf.-PLZ":"Empf.-PLZ",
        "Empf.-Ort":"Empf.-Ort",
        "Empf.-Str.":"Empf.-Str.",
        "Empf.-Str.-Nr.":"Empf.-Str.-Nr.",
        "customer_Ladung_lange_cm":"customer_lange_cm",# Mapped key to new internal processing name
        "customer_Ladung_breite_cm":"customer_breite_cm",# Mapped key to new internal processing name
        "customer_Ladung_hohe_cm":"customer_hohe_cm",# Mapped key to new internal processing name
        "customer_Ladung_einheit":"customer_einheit",# Mapped key to new internal processing name
        "Menge_Colli":"customer_menge",# Mapped key to new internal processing name
        "Telefonnummer_Kontaktperson_Entladung":"customer_telefonnummer", # Mapped key to new internal processing name
        "Beschreibung_des_Materials_bzw_Ladung":"customer_beschreibung" # Mapped key to new internal processing name
        },
    "Kemmler": {
        "Dispobereich":"customer_branch_cluster",
        "Entl. von  (Auftr.)":"Entl. von  (Auftr.)",
        "Entl. bis (Auftr.)":"Entl. bis (Auftr.)",
        
        "customer_Lieferschein":"customer_Lieferschein",
        
        "Auftr.-Nr.":"Auftr.-Nr.",
        "Entladeart":"Entladeart",
        "Menge [kg] (Auftrag)":"customer_shipment_weight_kg", # Mapped key to new internal processing name
        "komiss.  Menge aus LVS":"customer_shipment_volume_units", # Mapped key to new internal processing name
        
        "Fahrerhinweis (Auftr.)":"Fahrerhinweis (Auftr.)",
        "Anm. Lieferzeit":"Anm. Lieferzeit",
        "Vers.-Str.":"Vers.-Str.",
        "Vers.-Str.-Nr.":"Vers.-Str.-Nr.",
        "Vers.-PLZ":"Vers.-PLZ",
        "Vers.-Name":"Vers.-Name",
        "Vers.-Ort":"Vers.-Ort",
        "Empfänger":"Empfänger",
        "Empf.-PLZ":"Empf.-PLZ",
        "Empf.-Ort":"Empf.-Ort",
        "Empf.-Str.":"Empf.-Str.",
        "Empf.-Str.-Nr.":"Empf.-Str.-Nr.",
        
        "customer_Ladung_lange_cm":"customer_lange_cm",# Mapped key to new internal processing name
        "customer_Ladung_breite_cm":"customer_breite_cm",# Mapped key to new internal processing name
        "customer_Ladung_hohe_cm":"customer_hohe_cm",# Mapped key to new internal processing name
        "customer_Ladung_einheit":"customer_einheit",# Mapped key to new internal processing name
        "Menge_Colli":"customer_menge",# Mapped key to new internal processing name
        "Telefonnummer_Kontaktperson_Entladung":"customer_telefonnummer", # Mapped key to new internal processing name
        "Beschreibung_des_Materials_bzw_Ladung":"customer_beschreibung" # Mapped key to new internal processing name
        },
    "laminatDepot": { 
        "Filiale":"customer_branch_cluster",
        "Lieferdatum":"Entl. bis (Auftr.)",
        
        "Vermerk":"customer_Lieferschein", # needs to be checked
        
        "Interne Auftragsnummer":"Auftr.-Nr.",
        "Gewicht":"customer_shipment_weight_kg", # Mapped key to new internal processing name
        "Lasteinheiten":"customer_shipment_volume_units", # Mapped key to new internal processing name
        
        "Ansprechpartner":"Empfänger",
        "PLZ":"Empf.-PLZ",
        "Ort":"Empf.-Ort",
        "Straße":"Empf.-Str.",
        "Hausnummer":"Empf.-Str.-Nr.",
        
        #"Menge_Colli":"customer_menge",# Mapped key to new internal processing name
        "Telefonnummer":"customer_telefonnummer", # Mapped key to new internal processing name
        "Position":"customer_beschreibung" # Mapped key to new internal processing name
        },
    "laminatDepot_MultiBranch": { 
        "Filiale":"customer_branch_cluster",
        "Lieferdatum":"Entl. bis (Auftr.)",
        
        "Vermerk":"customer_Lieferschein", # needs to be checked
        
        "Interne Auftragsnummer":"Auftr.-Nr.",
        "Gewicht":"customer_shipment_weight_kg", # Mapped key to new internal processing name
        "Lasteinheiten":"customer_shipment_volume_units", # Mapped key to new internal processing name
        
        "Ansprechpartner":"Empfänger",
        "PLZ":"Empf.-PLZ",
        "Ort":"Empf.-Ort",
        "Straße":"Empf.-Str.",
        "Hausnummer":"Empf.-Str.-Nr.",
        
        #"Menge_Colli":"customer_menge",# Mapped key to new internal processing name
        "Telefonnummer":"customer_telefonnummer", # Mapped key to new internal processing name
        "Position":"customer_beschreibung" # Mapped key to new internal processing name
        },
    "Wigger": {
        "Dispobereich":"customer_branch_cluster",
        "Entl. von  (Auftr.)":"Entl. von  (Auftr.)",
        "Entl. bis (Auftr.)":"Entl. bis (Auftr.)",
        
        "customer_Lieferschein":"customer_Lieferschein",
        
        "Auftr.-Nr.":"Auftr.-Nr.",
        "Entladeart":"Entladeart",
        "Menge [kg] (Auftrag)":"customer_shipment_weight_kg", # Mapped key to new internal processing name
        "komiss.  Menge aus LVS":"customer_shipment_volume_units", # Mapped key to new internal processing name
        
        "Fahrerhinweis (Auftr.)":"Fahrerhinweis (Auftr.)",
        "Anm. Lieferzeit":"Anm. Lieferzeit",
        "Vers.-Str.":"Vers.-Str.",
        "Vers.-Str.-Nr.":"Vers.-Str.-Nr.",
        "Vers.-PLZ":"Vers.-PLZ",
        "Vers.-Name":"Vers.-Name",
        "Vers.-Ort":"Vers.-Ort",
        "Empfänger":"Empfänger",
        "Empf.-PLZ":"Empf.-PLZ",
        "Empf.-Ort":"Empf.-Ort",
        "Empf.-Str.":"Empf.-Str.",
        "Empf.-Str.-Nr.":"Empf.-Str.-Nr.",
        
        "customer_Ladung_lange_cm":"customer_lange_cm",# Mapped key to new internal processing name
        "customer_Ladung_breite_cm":"customer_breite_cm",# Mapped key to new internal processing name
        "customer_Ladung_hohe_cm":"customer_hohe_cm",# Mapped key to new internal processing name
        "customer_Ladung_einheit":"customer_einheit",# Mapped key to new internal processing name
        "Menge_Colli":"customer_menge",# Mapped key to new internal processing name
        "Telefonnummer_Kontaktperson_Entladung":"customer_telefonnummer", # Mapped key to new internal processing name
        "Beschreibung_des_Materials_bzw_Ladung":"customer_beschreibung" # Mapped key to new internal processing name
    },
    "Obi_Buchholz": {
        "Dispobereich":"customer_branch_cluster",
        "Entl. von  (Auftr.)":"Entl. von  (Auftr.)",
        "Entl. bis (Auftr.)":"Entl. bis (Auftr.)",
        
        "customer_Lieferschein":"customer_Lieferschein",
        
        "Auftr.-Nr.":"Auftr.-Nr.",
        "Entladeart":"Entladeart",
        "Menge [kg] (Auftrag)":"customer_shipment_weight_kg", # Mapped key to new internal processing name
        "komiss.  Menge aus LVS":"customer_shipment_volume_units", # Mapped key to new internal processing name
        
        "Fahrerhinweis (Auftr.)":"Fahrerhinweis (Auftr.)",
        "Anm. Lieferzeit":"Anm. Lieferzeit",
        "Vers.-Str.":"Vers.-Str.",
        "Vers.-Str.-Nr.":"Vers.-Str.-Nr.",
        "Vers.-PLZ":"Vers.-PLZ",
        "Vers.-Name":"Vers.-Name",
        "Vers.-Ort":"Vers.-Ort",
        "Empfänger":"Empfänger",
        "Empf.-PLZ":"Empf.-PLZ",
        "Empf.-Ort":"Empf.-Ort",
        "Empf.-Str.":"Empf.-Str.",
        "Empf.-Str.-Nr.":"Empf.-Str.-Nr.",
        
        "customer_Ladung_lange_cm":"customer_lange_cm",# Mapped key to new internal processing name
        "customer_Ladung_breite_cm":"customer_breite_cm",# Mapped key to new internal processing name
        "customer_Ladung_hohe_cm":"customer_hohe_cm",# Mapped key to new internal processing name
        "customer_Ladung_einheit":"customer_einheit",# Mapped key to new internal processing name
        "Menge_Colli":"customer_menge",# Mapped key to new internal processing name
        "Telefonnummer_Kontaktperson_Entladung":"customer_telefonnummer", # Mapped key to new internal processing name
        "Beschreibung_des_Materials_bzw_Ladung":"customer_beschreibung" # Mapped key to new internal processing name
    }
}

# The get_column_mapping function retrieves the appropriate mapping for a given client.
# If no mapping is found for the client, it returns an empty dictionary.
def get_column_mapping(client_name: str):
    """
    Retrieve the column mapping for a specific client.

    Args:
        client_name (str): The name of the client.

    Returns:
        dict: The column mapping for the client.
    """
    return CLIENT_COLUMN_MAPPINGS.get(client_name, {})
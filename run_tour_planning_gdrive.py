#!/usr/bin/env python3
"""
Local runner for Tour Planning Script - Using Google Drive paths directly
This version uses your synced Google Drive files without copying them.
"""

import os
import sys
from pathlib import Path
# Optional: Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional

# Add current directory to path for module imports
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
from module_upload import upload_excel
from module_clean import clean_and_process_data
from module_geocoding import geocoding_cleaned_data
from module_vrp import vrp_problem_definition, vrp_problem_execution
from module_results import merge_results
from module_export import create_bexos_import_csv
from module_map import create_map
import math

def replace_nan_with_none_recursive(obj):
    """Recursively replaces NaN and Inf float values in a nested dict/list with None."""
    if isinstance(obj, dict):
        return {k: replace_nan_with_none_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_none_recursive(elem) for elem in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj

def main():
    """Main execution function - Uses Google Drive paths directly"""
    
    # ============================================================================
    # CONFIGURATION
    # ============================================================================
    
    # Get API key from environment variable
    api_key = os.getenv('HERE_API_KEY')
    if not api_key:
        print("ERROR: HERE_API_KEY environment variable not set!")
        print("Set it with: export HERE_API_KEY='your_key_here'")
        print("Or create a .env file with: HERE_API_KEY=your_key_here")
        sys.exit(1)
    
    # Planning parameters
    base_date_str = "2025-12-15"  # Format: YYYY-MM-DD
    client_name = "Kemmler"  # Options: Stark, Kemmler, laminatDepot_MultiBranch, Wigger, Obi_Buchholz, default
    product_category = "Ohne Modifikation"  # Options: Ohne Modifikation, bex Kurier, bex Tour
    
    # ============================================================================
    # GOOGLE DRIVE PATHS - Uses your synced Google Drive directly
    # ============================================================================
    
    # Google Drive base path (adjust if your path is different)
    google_drive_base = Path("/Users/oliverroscher/Library/CloudStorage/GoogleDrive-oliver.brenningmeyer@bexapp.de/Meine Ablage/Colab Notebooks")
    
    # Set paths based on client (matching Colab structure)
    if client_name == "Stark":
        depots_path = google_drive_base / "stark" / "depots" / "Depots_geocoded.xlsx"
        output_folder_path = google_drive_base / "stark" / base_date_str
        input_file = google_drive_base / "stark" / "Kemmler - Auftragsspeicher - Touren.xlsx"  # Adjust filename
        sheet_name = 'Sheet1'
    elif client_name == "Kemmler":
        depots_path = google_drive_base / "kemmler" / "depots" / "Depots_geocoded.xlsx"
        output_folder_path = google_drive_base / "kemmler" / base_date_str
        input_file = google_drive_base / "kemmler" / "Kemmler - Auftragsspeicher - Touren.xlsx"
        sheet_name = 'Touren - BEX'
    elif client_name == "laminatDepot_MultiBranch":
        depots_path = google_drive_base / "laminatdepot" / "depots" / "Depots_geocoded.xlsx"
        output_folder_path = google_drive_base / "laminatdepot" / base_date_str
        input_file = google_drive_base / "laminatdepot" / "orders.xlsx"  # Adjust filename
        sheet_name = 'input'
    elif client_name == "Wigger":
        depots_path = google_drive_base / "Wigger" / "depots" / "Depots_geocoded.xlsx"
        output_folder_path = google_drive_base / "Wigger" / base_date_str
        input_file = google_drive_base / "Wigger" / "orders.xlsx"  # Adjust filename
        sheet_name = 'Touren - BEX'
    elif client_name == "Obi_Buchholz":
        depots_path = google_drive_base / "Obi_Buchholz" / "depots" / "Depots_geocoded.xlsx"
        output_folder_path = google_drive_base / "Obi_Buchholz" / base_date_str
        input_file = google_drive_base / "Obi_Buchholz" / "orders.xlsx"  # Adjust filename
        sheet_name = 'Touren - BEX'
    else:
        depots_path = google_drive_base / "generic_tourplanning" / "depots" / "Depots_geocoded.xlsx"
        output_folder_path = google_drive_base / "generic_tourplanning" / base_date_str
        input_file = google_drive_base / "generic_tourplanning" / "orders.xlsx"  # Adjust filename
        sheet_name = 'Sheet1'
    
    # Convert Path objects to strings
    depots_path = str(depots_path)
    output_folder_path = str(output_folder_path)
    input_file = str(input_file)
    
    # ============================================================================
    # EXECUTION PIPELINE (same as regular script)
    # ============================================================================
    
    print("=" * 70)
    print("Tour Planning Script - Local Execution (Google Drive)")
    print("=" * 70)
    print(f"Client: {client_name}")
    print(f"Date: {base_date_str}")
    print(f"Input file: {input_file}")
    print(f"Depots file: {depots_path}")
    print(f"Output folder: {output_folder_path}")
    print("=" * 70)
    print()
    
    try:
        # Step 1: Upload and load data
        print("Step 1: Loading input file...")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        df_raw = upload_excel(input_file, sheet_name=sheet_name)
        print(f"✓ Loaded {len(df_raw)} rows from {input_file}")
        print()
        
        # Step 2: Clean data
        print("Step 2: Cleaning and processing data...")
        df_clean = clean_and_process_data(df_raw, base_date_str, output_folder_path, client_name)
        print(f"✓ Cleaned data: {len(df_clean)} rows")
        print()
        
        # Step 3: Geocode addresses
        print("Step 3: Geocoding addresses...")
        df_geocoded = geocoding_cleaned_data(df_clean, api_key, client_name)
        print(f"✓ Geocoded {len(df_geocoded)} addresses")
        print()
        
        # Step 4: Create VRP problem
        print("Step 4: Creating VRP problem definition...")
        vrp_problem = vrp_problem_definition(
            df_geocoded, api_key, depots_path, base_date_str, 
            product_category, client_name
        )
        print("✓ VRP problem definition created")
        print()
        
        # Step 5: Execute VRP
        print("Step 5: Executing VRP optimization...")
        vrp_problem_cleaned = replace_nan_with_none_recursive(vrp_problem)
        vrp_response = vrp_problem_execution(vrp_problem_cleaned, api_key)
        print("✓ VRP optimization completed")
        print()
        
        # Step 6: Merge results
        print("Step 6: Merging results...")
        merged_df, df_unassigned_jobs = merge_results(
            vrp_response, df_geocoded, output_folder_path, depots_path
        )
        print(f"✓ Merged {len(merged_df)} activities")
        print(f"  Unassigned jobs: {len(df_unassigned_jobs)}")
        print()
        
        # Step 7: Export results
        print("Step 7: Exporting results...")
        # Save full results
        output_csv = os.path.join(output_folder_path, f"{base_date_str}.csv")
        merged_df.to_csv(output_csv, index=False)
        print(f"✓ Saved: {output_csv}")
        
        # Save bexOS import file
        bexos_df = create_bexos_import_csv(merged_df)
        bexos_csv = os.path.join(output_folder_path, f"{base_date_str}_import_to_bexOS.csv")
        bexos_df.to_csv(bexos_csv, index=False, sep=",", encoding="utf-8")
        print(f"✓ Saved: {bexos_csv}")
        print()
        
        # Step 8: Create map
        print("Step 8: Creating visualization map...")
        map_obj = create_map(merged_df, df_geocoded, df_unassigned_jobs, base_date_str)
        map_html = os.path.join(output_folder_path, f"{base_date_str}_tours_map.html")
        map_obj.save(map_html)
        print(f"✓ Saved: {map_html}")
        print()
        
        print("=" * 70)
        print("✓ Tour planning completed successfully!")
        print(f"Results saved to: {output_folder_path}")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("\nPlease check:")
        print("1. Input file path is correct")
        print("2. Depots file exists")
        print("3. Google Drive is synced and accessible")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


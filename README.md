# Tour Planning Modules

A modular Python system for vehicle routing optimization that processes delivery orders and creates optimized tour plans using the HERE Tour Planning API. The system is designed for logistics companies managing delivery operations across multiple clients with different configurations and requirements.

## Overview

This system automates the entire workflow from raw order data to optimized vehicle routes, generating tour plans that can be directly imported into bexOS (operational system). It supports multiple clients with client-specific configurations, column mappings, and business rules.

## Features

- **Multi-Client Support**: Handles different clients (Kemmler, Stark, Wigger, Obi_Buchholz, laminatDepot_MultiBranch) with unique configurations
- **Territory-Based Routing**: Vehicles can be restricted to specific territories with strict or flexible boundaries
- **Flexible Fleet Management**: Supports both dedicated depot vehicles and open vehicles
- **Skills Matching**: Matches jobs requiring specific vehicle capabilities (e.g., tail lift)
- **Time Window Constraints**: Respects delivery time windows from order data
- **Capacity Management**: Handles volume and weight constraints
- **Advanced Optimization**: Multiple optimization objectives (minimize cost, tours, unassigned jobs; balance duration; maximize territory jobs)
- **Interactive Visualization**: Generates interactive maps showing optimized routes

## Quick Start (Google Colab)

### Prerequisites

1. **Google Drive Setup**: 
   - Upload this repository to your Google Drive at: `MyDrive/Colab Notebooks/tourplanning_modules/`
   - Ensure your client data folders are organized as:
     ```
     MyDrive/Colab Notebooks/
     ├── tourplanning_modules/          # This repository
     ├── {client_name}/
     │   ├── depots/
     │   │   └── Depots_geocoded.xlsx
     │   └── {date}/                    # Output folder (created automatically)
     ```

2. **HERE API Key**:
   - Get your HERE API key from [HERE Developer Portal](https://developer.here.com/)
   - Store it in Google Colab Secrets:
     - Go to Colab → 🔑 (Secrets) → Add new secret
     - Name: `apiKey_HERE`
     - Value: Your HERE API key

3. **Open the Notebook**:
   - Open `TourPlanning_Script.ipynb` in Google Colab
   - The notebook will automatically:
     - Mount your Google Drive
     - Load all modules from the repository
     - Set up paths based on your client selection

### First Run

1. Run the first cell to mount Drive and load modules
2. Select your client name and planning date using the form widgets
3. Upload your order Excel file when prompted
4. Execute cells sequentially to run the full pipeline

**Note**: All data paths are configured to work with the Google Drive structure. Do not modify the path structure in the notebook.

## Architecture

The system is built as a modular pipeline where each module handles a specific step in the tour planning process:

```
Excel Upload → Data Cleaning → Geocoding → VRP Problem Definition → 
VRP Execution → Results Merging → Export → Visualization
```

## Modules

### 1. `module_upload.py`
Handles Excel file uploads and loading.

**Functions:**
- `upload_excel(path, sheet_name)`: Load Excel file from local path
- `upload_excel_via_widget(sheet_name)`: Interactive file upload via Google Colab widget

### 2. `module_clean.py`
Performs data cleaning, normalization, and preprocessing.

**Key Functions:**
- `normalize_column_names()`: Maps client-specific columns to standardized names
- `clean_and_process_data()`: Main cleaning pipeline that:
  - Normalizes column names based on client mapping
  - Filters by date and branch clusters
  - Converts time windows to ISO 8601 format
  - Handles missing values and data type conversions
  - Adjusts volume units based on client configuration
  - Fills default values for required columns

### 3. `module_column_mapping.py`
Maps client-specific column names to standardized internal column names.

**Supported Clients:**
- Stark
- Kemmler
- Wigger
- Obi_Buchholz
- laminatDepot_MultiBranch

**Function:**
- `get_column_mapping(client_name)`: Returns column mapping dictionary for specified client

### 4. `module_geocoding.py`
Geocodes pickup and delivery addresses using HERE Geocoding API.

**Features:**
- Rate limit handling with exponential backoff
- Address caching to avoid duplicate API calls
- Configurable geocoding (can skip pickup if predefined locations)
- Handles both pickup and dropoff locations

**Function:**
- `geocoding_cleaned_data(df, api_key, client_name)`: Geocodes addresses and adds lat/lng columns

### 5. `module_vrp.py`
Creates and executes Vehicle Routing Problem (VRP) optimization requests.

**Functions:**
- `vrp_problem_definition()`: Builds VRP problem JSON with:
  - Fleet configuration (dedicated vehicles from depots, open vehicles)
  - Job definitions (pickups, deliveries, time windows, demands, skills)
  - Territory assignments
  - Shift configurations
- `vrp_problem_execution()`: Sends request to HERE Tour Planning API and returns results

**Fleet Types:**
- **Dedicated Vehicles**: Assigned to specific depots with defined shifts (fullDay/halfDay)
- **Open Vehicles**: Flexible fleet available for any job

**Job Requirements:**
- Pickup and delivery locations
- Time windows
- Volume and weight demands
- Required vehicle skills
- Territory assignments

### 6. `module_results.py`
Merges VRP optimization results with original order data.

**Function:**
- `merge_results()`: 
  - Extracts activities from VRP response tours
  - Joins with geocoded order data
  - Normalizes location data (pickup/delivery)
  - Identifies unassigned jobs with reasons
  - Enriches with depot information

### 7. `module_export.py`
Creates export files for bexOS import.

**Function:**
- `create_bexos_import_csv()`: Maps internal columns to bexOS format and creates export-ready DataFrame

### 8. `module_map.py`
Creates interactive map visualizations using Folium.

**Function:**
- `create_map()`: Generates interactive map showing:
  - Vehicle routes with color-coded polylines
  - Stop markers with activity details
  - Unassigned orders
  - Vehicle legend

### 9. `module_client_configuration.py`
Centralized configuration for all clients.

**Configuration Sections:**
- **Order**: Time windows, volume unit size, default values
- **Geocoding**: Pickup/dropoff geocoding preferences
- **Dedicated Branches**: Predefined pickup locations per cluster
- **Break Settings**: Duration and times for fullDay/halfDay shifts
- **Fleet**: Vehicle costs, capacities, limits, shifts
- **Job**: Pickup and delivery durations
- **Advanced Objectives**: Optimization priorities

## Requirements

### For Google Colab

Dependencies are automatically installed in Colab. If you need to install manually:

```python
!pip install pandas openpyxl numpy networkx matplotlib requests folium
```

### For Local Development

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `pandas`: Data manipulation
- `openpyxl`: Excel file handling
- `numpy`: Numerical operations
- `networkx`: Graph operations
- `matplotlib`: Plotting
- `requests`: API calls
- `folium`: Map visualization

## Repository Structure

```
tourplanning_modules/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── __init__.py                        # Package initialization
├── TourPlanning_Script.ipynb         # Main execution notebook
├── module_upload.py                   # File upload module
├── module_clean.py                    # Data cleaning module
├── module_column_mapping.py           # Column mapping module
├── module_geocoding.py                # Geocoding module
├── module_vrp.py                      # VRP optimization module
├── module_results.py                  # Results processing module
├── module_export.py                   # Export module
├── module_map.py                      # Map visualization module
└── module_client_configuration.py     # Client configuration module
```

## Usage

### Basic Workflow (Google Colab)

1. **Initialize and Load Modules**
   ```python
   from google.colab import drive
   import sys
   
   drive.mount('/content/drive')
   sys.path.insert(0, '/content/drive/MyDrive/Colab Notebooks/tourplanning_modules')
   
   import module_upload, module_clean, module_geocoding, module_vrp, \
          module_results, module_map, module_export, module_client_configuration
   ```

2. **Set Parameters**
   ```python
   api_key = userdata.get('apiKey_HERE')
   base_date_str = "2025-12-15"
   client_name = "Kemmler"
   product_category = "bex Tour"
   depots_path = '/path/to/depots.xlsx'
   output_folder_path = '/path/to/output'
   ```

3. **Upload and Process Data**
   ```python
   # Upload Excel file
   df_raw = module_upload.upload_excel_via_widget(sheet_name='Sheet1')
   
   # Clean data
   df_clean = module_clean.clean_and_process_data(
       df_raw, base_date_str, output_folder_path, client_name
   )
   
   # Geocode addresses
   df_geocoded = module_geocoding.geocoding_cleaned_data(
       df_clean, api_key, client_name
   )
   ```

4. **Run VRP Optimization**
   ```python
   # Create VRP problem
   vrp_problem = module_vrp.vrp_problem_definition(
       df_geocoded, api_key, depots_path, base_date_str, 
       product_category, client_name
   )
   
   # Execute optimization
   vrp_response = module_vrp.vrp_problem_execution(vrp_problem, api_key)
   ```

5. **Process and Export Results**
   ```python
   # Merge results
   merged_df, unassigned = module_results.merge_results(
       vrp_response, df_geocoded, output_folder_path, depots_path
   )
   
   # Export to CSV
   merged_df.to_csv(f'{output_folder_path}/{base_date_str}.csv')
   
   # Create bexOS export
   bexos_df = module_export.create_bexos_import_csv(merged_df)
   bexos_df.to_csv(f'{output_folder_path}/{base_date_str}_import_to_bexOS.csv', 
                   index=False, sep=",", encoding="utf-8")
   ```

6. **Visualize Results**
   ```python
   # Create map
   map = module_map.create_map(merged_df, df_geocoded, unassigned, base_date_str)
   map.save(f'{output_folder_path}/{base_date_str}_tours_map.html')
   ```

## Configuration

Client-specific configurations are stored in `module_client_configuration.py`. Each client can have:

- **Order Settings**: Time windows, volume unit size, default column values
- **Fleet Configuration**: 
  - Dedicated vehicles: Costs, capacities, shift times, territory restrictions
  - Open vehicles: Available fleet with skills and capacities
- **Job Settings**: Pickup and delivery durations
- **Break Settings**: Duration and time windows for breaks
- **Optimization Objectives**: Priority order for optimization goals
- **Geocoding Settings**: Which locations need geocoding
- **Dedicated Branches**: Predefined pickup locations per cluster

### Adding a New Client

1. Add column mapping in `module_column_mapping.py`:
   ```python
   CLIENT_COLUMN_MAPPINGS["NewClient"] = {
       "RawColumnName": "standardized_column_name",
       # ... more mappings
   }
   ```

2. Add configuration in `module_client_configuration.py`:
   ```python
   CONFIG["NewClient"] = {
       "order": {...},
       "fleet": {...},
       "job": {...},
       # ... other settings
   }
   ```

## Important Notes

⚠️ **Path Structure**: The notebook uses hardcoded Google Drive paths that match the expected folder structure. **Do not modify these paths** in the notebook, as they are essential for:
- Accessing depot files
- Saving output files
- Loading modules correctly

The paths are structured as:
- Modules: `/content/drive/MyDrive/Colab Notebooks/tourplanning_modules/`
- Client data: `/content/drive/MyDrive/Colab Notebooks/{client_name}/`
- Depots: `/content/drive/MyDrive/Colab Notebooks/{client_name}/depots/`
- Output: `/content/drive/MyDrive/Colab Notebooks/{client_name}/{date}/`

## Data Requirements

### Order Data (Excel)
Required columns (after mapping):
- `Auftr.-Nr.`: Order number
- `customer_branch_cluster`: Territory/branch cluster
- `Entl. von (Auftr.)`: Delivery time window start
- `Entl. bis (Auftr.)`: Delivery time window end
- `customer_shipment_weight_kg`: Weight in kg
- `customer_shipment_volume_units`: Volume in standardized units
- `Vers.-Str.`, `Vers.-PLZ`, `Vers.-Ort`: Pickup address
- `Empf.-Str.`, `Empf.-PLZ`, `Empf.-Ort`: Delivery address
- `Entladeart`: Unloading type (determines required skills)

### Depot Data (Excel)
Required columns:
- `Dispobereich`: Territory identifier
- `active_Dispobereich`: Active flag
- `here_lat`, `here_lng`: Depot coordinates
- `count_fullDay`, `count_halfDay`: Vehicle counts
- `startTime_fullDay`, `endTime_fullDay`: Shift times
- `price_fullDay`, `price_halfDay`: Vehicle costs
- `capacity_fullDay`, `capacity_halfDay`: Capacities
- `salesVehicleClass_fullDay`, `salesVehicleClass_halfDay`: Vehicle skills

## Output Files

The system generates several output files:

1. **`{date}.csv`**: Complete merged results with all VRP and order data
2. **`{date}_import_to_bexOS.csv`**: Formatted export for bexOS import
3. **`{date}_tours_map.html`**: Interactive map visualization

## API Requirements

- **HERE Geocoding API**: For address geocoding
- **HERE Tour Planning API**: For VRP optimization

Both require API keys stored in Google Colab secrets or environment variables.

## Supported Clients

- **Kemmler**: Full configuration with dedicated and open vehicles
- **Stark**: Standard configuration
- **Wigger**: Extended shift times and distance limits
- **Obi_Buchholz**: Standard configuration
- **laminatDepot_MultiBranch**: Multi-branch with predefined pickup locations

## Notes

- The system is designed for use in Google Colab but can be adapted for local use
- All dates should be in `YYYY-MM-DD` format
- Time windows are converted to ISO 8601 format for API compatibility
- Volume units are standardized (multiplied by 10) for internal processing
- The system handles rate limiting and retries for HERE API calls
- Unassigned jobs are tracked with reasons for analysis

## License

[Add license information here]

## Contact

Oliver Brenningmeyer
oliver.brenningmeyer@bexapp.de


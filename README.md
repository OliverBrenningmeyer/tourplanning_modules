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

## Running Locally vs. Google Colab

This system can run both **locally** on your machine and in **Google Colab**. 

- **Google Colab**: Best for quick runs, sharing, and when you need the interactive file upload widget
- **Local**: Best for faster execution, offline work, better debugging, and production use

### Quick Start (Local)

For the fastest local setup, see [QUICK_RUN.md](QUICK_RUN.md). For detailed instructions, see [LOCAL_SETUP.md](LOCAL_SETUP.md).

**Note**: The `venv/`, `__pycache__/`, and `.vscode/` folders are not needed for execution and are excluded from version control. Create your own virtual environment if needed.

**Quick commands:**
```bash
# Set API key
export HERE_API_KEY='your_api_key_here'

# Run with Google Drive paths (if synced locally)
python3 run_tour_planning_gdrive.py

# Or run with local data folder
python3 run_tour_planning.py

# Or use the quick run script
./run.sh
```

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
     │   └── outputs/                   # Output directory (create manually)
     │       └── {date}/                # Date folders (created automatically)
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

### 10. `module_input_validation.py`
Validates input files and data quality before processing.

**Features:**
- Validates Excel file structure and required columns
- Checks data quality (missing values, date formats, numeric values)
- Validates depot files
- Provides detailed error messages and warnings
- Validates geocoding results

**Functions:**
- `validate_input_file()`: Validates uploaded Excel file
- `InputValidator`: Class for comprehensive validation with detailed error reporting

### 11. `module_status_tracker.py`
Tracks the status of the tour planning process with progress indicators and error reporting.

**Features:**
- Tracks each processing step with status (success/error/warning)
- Records errors and warnings with details
- Provides process summary with duration
- Can export status to DataFrame

**Functions:**
- `StatusTracker`: Class for tracking process status
- `get_tracker()`: Get global status tracker instance
- `reset_tracker()`: Reset tracker for re-runs

### 12. `module_tour_summary.py`
Generates and displays tour planning statistics and summaries.

**Features:**
- Creates summary statistics for each tour (distance, duration, stops, jobs)
- Displays formatted tour summaries
- Shows unassigned jobs with reasons
- Calculates totals across all tours

**Functions:**
- `generate_tour_summary()`: Creates DataFrame with tour statistics
- `display_tour_summary()`: Displays formatted summary

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
- `python-dotenv`: Environment variable management (for local execution)

## Repository Structure

```
tourplanning_modules/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── __init__.py                        # Package initialization
├── TourPlanning_Script.ipynb         # Main execution notebook (Colab)
├── run_tour_planning.py               # Local execution script (uses data/ folder)
├── run_tour_planning_gdrive.py        # Local execution script (uses Google Drive paths)
├── run.sh                             # Quick run bash script
├── setup_local.sh                     # Local setup helper script
├── LOCAL_SETUP.md                     # Detailed local setup guide
├── QUICK_RUN.md                       # Quick run guide
├── SETUP.md                           # GitHub repository setup guide
├── module_upload.py                   # File upload module
├── module_clean.py                    # Data cleaning module
├── module_column_mapping.py           # Column mapping module
├── module_geocoding.py                # Geocoding module
├── module_vrp.py                      # VRP optimization module
├── module_results.py                  # Results processing module
├── module_export.py                   # Export module
├── module_map.py                      # Map visualization module
├── module_client_configuration.py     # Client configuration module
├── module_input_validation.py         # Input validation module
├── module_status_tracker.py           # Status tracking module
├── module_tour_summary.py             # Tour summary module
└── data/                              # Local data directory (for local execution)
    ├── README.md                      # Data structure documentation
    └── {client_name}/
        ├── depots/
        │   └── Depots_geocoded.xlsx    # Required: Depot configuration
        └── outputs/                   # Output directory (auto-created, not tracked)
            └── {date}/                # Date-based output folders
                ├── {date}.csv
                ├── {date}_import_to_bexOS.csv
                └── {date}_tours_map.html
```

## Usage

### Basic Workflow (Local Execution)

**Option 1: Using Google Drive paths (if synced locally)**
```bash
# Set API key
export HERE_API_KEY='your_api_key_here'

# Run the script
python3 run_tour_planning_gdrive.py
```

**Option 2: Using local data folder**
```bash
# Set API key
export HERE_API_KEY='your_api_key_here'

# Copy your data files to data/{client_name}/ first
# Then run:
python3 run_tour_planning.py
```

**Option 3: Using quick run script**
```bash
# Set API key first
export HERE_API_KEY='your_api_key_here'

# Run
./run.sh
```

**Configuration:**
- Edit `run_tour_planning.py` or `run_tour_planning_gdrive.py` to change:
  - `client_name`: Client name (Kemmler, Stark, Wigger, etc.)
  - `base_date_str`: Planning date (YYYY-MM-DD format)
  - `product_category`: Product category
  - File paths (if needed)

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
   
   # Validate input (optional but recommended)
   from module_input_validation import validate_input_file
   is_valid, errors, warnings = validate_input_file(df_raw, client_name, sheet_name)
   if not is_valid:
       print("Validation errors:", errors)
       # Handle errors...
   
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
   
   # Display tour summary (optional)
   from module_tour_summary import display_tour_summary
   display_tour_summary(vrp_response, merged_df, unassigned, base_date_str)
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
- Output: `/content/drive/MyDrive/Colab Notebooks/{client_name}/outputs/{date}/`

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

The system generates several output files in `data/{client}/outputs/{date}/`:

1. **`{date}.csv`**: Complete merged results with all VRP and order data
2. **`{date}_import_to_bexOS.csv`**: Formatted export for bexOS import
3. **`{date}_tours_map.html`**: Interactive map visualization

**Note**: Output files are not tracked in version control (see `.gitignore`). Only depot configuration files are tracked.

## Local Execution Scripts

The repository includes several scripts for local execution:

### `run_tour_planning.py`
Main local execution script that uses a local `data/` folder structure. Configure client name, date, and paths in the script.

### `run_tour_planning_gdrive.py`
Local execution script that uses Google Drive paths directly (if Google Drive is synced locally). This is convenient if you want to use the same files as Colab without copying them.

### `run.sh`
Quick bash script that checks for API key and runs `run_tour_planning_gdrive.py`. Make it executable with `chmod +x run.sh`.

### Setup Scripts
- `setup_local.sh`: Helper script for initial local setup
- See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed setup instructions

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

- The system works in both **Google Colab** and **locally** - see [LOCAL_SETUP.md](LOCAL_SETUP.md) for local setup
- All dates should be in `YYYY-MM-DD` format
- Time windows are converted to ISO 8601 format for API compatibility
- Volume units are standardized (multiplied by 10) for internal processing
- The system handles rate limiting and retries for HERE API calls
- Unassigned jobs are tracked with reasons for analysis
- Input validation is available via `module_input_validation` to catch errors early
- Status tracking via `module_status_tracker` provides detailed process monitoring
- Tour summaries via `module_tour_summary` provide quick statistics overview

## Additional Documentation

- **[LOCAL_SETUP.md](LOCAL_SETUP.md)**: Detailed guide for local setup and execution
- **[QUICK_RUN.md](QUICK_RUN.md)**: Quick reference for running locally
- **[SETUP.md](SETUP.md)**: GitHub repository setup guide
- **[data/README.md](data/README.md)**: Data directory structure and organization

## License

[Add license information here]

## Contact

Oliver Brenningmeyer
oliver.brenningmeyer@bexapp.de


# Data Directory Structure

This directory contains client-specific data files for the tour planning system.

## Directory Structure

```
data/
├── {client_name}/
│   ├── depots/
│   │   └── Depots_geocoded.xlsx    # REQUIRED: Depot configuration file
│   └── outputs/                    # Execution outputs (auto-created)
│       └── {date}/                 # Date-based output folders (YYYY-MM-DD)
│           ├── {date}.csv
│           ├── {date}_import_to_bexOS.csv
│           └── {date}_tours_map.html
```

## Required Files

### Depot Files

Each client requires a depot configuration file:
- **Location**: `{client_name}/depots/Depots_geocoded.xlsx`
- **Required columns**: See main `README.md` for details
- **Status**: These files are tracked in version control (required for execution)

Required columns in depot files:
- `Dispobereich`: Territory identifier
- `active_Dispobereich`: Active flag
- `here_lat`, `here_lng`: Depot coordinates
- `count_fullDay`, `count_halfDay`: Vehicle counts
- `startTime_fullDay`, `endTime_fullDay`: Shift times
- `price_fullDay`, `price_halfDay`: Vehicle costs
- `capacity_fullDay`, `capacity_halfDay`: Capacities
- `salesVehicleClass_fullDay`, `salesVehicleClass_halfDay`: Vehicle skills

## Output Files

All execution outputs are automatically saved to:
- **Location**: `{client_name}/outputs/{date}/`

Output files include:
- `{date}.csv` - Complete merged results with all VRP and order data
- `{date}_import_to_bexOS.csv` - Formatted export for bexOS import
- `{date}_tours_map.html` - Interactive map visualization

**Note**: Output files are NOT tracked in version control (they are generated during execution).

## Input Files

Input order files should be:
- **Colab execution**: Uploaded via Colab widget (not stored in repo)
- **Local execution**: Placed in the client directory or specified via script configuration
- **Status**: NOT committed to repository (user-provided per run)

## Supported Clients

The following client directories are configured:
- `kemmler/`
- `stark/`
- `wigger/`
- `Obi_Buchholz/`
- `laminatdepot/`
- `generic_tourplanning/`

## Adding a New Client

1. Create directory: `data/{new_client_name}/`
2. Create depots folder: `data/{new_client_name}/depots/`
3. Add depot file: `data/{new_client_name}/depots/Depots_geocoded.xlsx`
4. Update execution scripts with new client configuration
5. Add client configuration to `module_client_configuration.py`
6. Add column mapping to `module_column_mapping.py`

## Notes

- Depot files are **required** for execution and are tracked in version control
- Output files are **generated** during execution and are NOT tracked
- Input order files are **user-provided** per run and are NOT tracked
- Date-based output folders are created automatically during execution


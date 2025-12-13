# Running Tour Planning Modules Locally

This guide explains how to run the tour planning system on your local machine without Google Colab.

## Prerequisites

1. **Python 3.8+** installed
2. **Git** (to clone the repository)
3. **HERE API Key** (same as used in Colab)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/OliverBrenningmeyer/tourplanning_modules.git
cd tourplanning_modules
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Set Up Your Data Structure

Create a local folder structure similar to your Google Drive:

```
tourplanning_modules/
├── data/
│   ├── {client_name}/
│   │   ├── depots/
│   │   │   └── Depots_geocoded.xlsx
│   │   └── {date}/              # Output folder (auto-created)
│   └── ...
└── ...
```

### 2. Set API Key

Create a `.env` file in the repository root:

```bash
echo "HERE_API_KEY=your_api_key_here" > .env
```

Or set it as an environment variable:

```bash
export HERE_API_KEY="your_api_key_here"
```

On Windows:
```cmd
set HERE_API_KEY=your_api_key_here
```

## Running Locally

### Option 1: Use the Python Script

Use the provided `run_tour_planning.py` script (see below for creation):

```bash
python run_tour_planning.py
```

### Option 2: Use Jupyter Notebook Locally

1. Install Jupyter:
   ```bash
   pip install jupyter
   ```

2. Open the notebook:
   ```bash
   jupyter notebook TourPlanning_Script.ipynb
   ```

3. Modify the first cell to remove Colab-specific code:
   - Remove `from google.colab import drive` and `drive.mount()`
   - Replace `userdata.get('apiKey_HERE')` with your API key
   - Update paths to point to your local data folders

### Option 3: Use as Python Module

Create your own script:

```python
import os
import sys
sys.path.insert(0, '.')

from module_upload import upload_excel
from module_clean import clean_and_process_data
from module_geocoding import geocoding_cleaned_data
from module_vrp import vrp_problem_definition, vrp_problem_execution
from module_results import merge_results
from module_export import create_bexos_import_csv
from module_map import create_map

# Configuration
api_key = os.getenv('HERE_API_KEY')
base_date_str = "2025-12-15"
client_name = "Kemmler"
product_category = "Ohne Modifikation"

# Set local paths
depots_path = './data/kemmler/depots/Depots_geocoded.xlsx'
output_folder_path = f'./data/kemmler/{base_date_str}'
input_file = './data/kemmler/orders.xlsx'
sheet_name = 'Touren - BEX'

# Run pipeline
df_raw = upload_excel(input_file, sheet_name=sheet_name)
df_clean = clean_and_process_data(df_raw, base_date_str, output_folder_path, client_name)
df_geocoded = geocoding_cleaned_data(df_clean, api_key, client_name)
vrp_problem = vrp_problem_definition(df_geocoded, api_key, depots_path, base_date_str, product_category, client_name)
vrp_response = vrp_problem_execution(vrp_problem, api_key)
merged_df, unassigned = merge_results(vrp_response, df_geocoded, output_folder_path, depots_path)

# Export
merged_df.to_csv(f'{output_folder_path}/{base_date_str}.csv')
bexos_df = create_bexos_import_csv(merged_df)
bexos_df.to_csv(f'{output_folder_path}/{base_date_str}_import_to_bexOS.csv', index=False, sep=",", encoding="utf-8")

# Create map
map_obj = create_map(merged_df, df_geocoded, unassigned, base_date_str)
map_obj.save(f'{output_folder_path}/{base_date_str}_tours_map.html')
```

## Differences from Colab

### 1. File Upload

In Colab, `upload_excel_via_widget()` uses Google Colab's file upload widget. Locally, use `upload_excel()` with a file path:

```python
# Colab
df = upload_excel_via_widget('Sheet1')

# Local
df = upload_excel('./data/orders.xlsx', sheet_name='Sheet1')
```

### 2. API Key

In Colab, API keys are stored in secrets. Locally, use environment variables or a `.env` file:

```python
# Colab
from google.colab import userdata
api_key = userdata.get('apiKey_HERE')

# Local
import os
api_key = os.getenv('HERE_API_KEY')
```

### 3. Paths

Colab uses `/content/drive/MyDrive/...` paths. Locally, use relative or absolute paths:

```python
# Colab
depots_path = '/content/drive/MyDrive/Colab Notebooks/kemmler/depots/Depots_geocoded.xlsx'

# Local
depots_path = './data/kemmler/depots/Depots_geocoded.xlsx'
# or
depots_path = '/Users/yourname/data/kemmler/depots/Depots_geocoded.xlsx'
```

### 4. Google Drive Mount

Colab mounts Google Drive. Locally, just use regular file paths - no mounting needed.

## Troubleshooting

### Module Import Errors

If modules can't be imported:
```python
import sys
sys.path.insert(0, '/path/to/tourplanning_modules')
```

### API Key Not Found

Make sure your API key is set:
```bash
echo $HERE_API_KEY  # Should show your key
```

### Path Errors

- Use absolute paths or paths relative to where you run the script
- Ensure all data files exist at the specified paths
- Create output directories if they don't exist (the code will create them automatically)

### Missing Dependencies

Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade
```

## Advantages of Running Locally

1. **Faster execution** - No network latency for file access
2. **Offline capability** - Work without internet (except for API calls)
3. **Better debugging** - Use your favorite IDE
4. **Version control** - Easier to track changes
5. **Customization** - Easier to modify and extend

## Disadvantages

1. **No interactive widgets** - File uploads must use file paths
2. **Manual setup** - Need to configure paths and API keys yourself
3. **Local resources** - Uses your machine's CPU/memory

## Next Steps

1. Set up your local data structure
2. Configure API key
3. Try running the example script
4. Customize paths and settings as needed


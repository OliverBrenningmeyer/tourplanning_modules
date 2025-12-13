# Tour Stop Order Editor

A tool for reordering stops within tours after VRP optimization in Google Colab.

## 📁 Folder Structure

```
tour_editor/
├── module_tour_editor.py      # Core module with all functions
├── README.md                   # This file
├── docs/
│   ├── TOUR_EDITOR_DESIGN.md   # Detailed design document
│   ├── TOUR_EDITOR_SUMMARY.md  # Quick reference
│   └── NOTEBOOK_INTEGRATION_EXAMPLE.md  # Integration examples
└── TourEditor_Standalone.ipynb # Standalone Colab notebook
```

## 🚀 Quick Start

### Option 1: Standalone Notebook (Recommended)

1. **Open the notebook:**
   - Open `TourEditor_Standalone.ipynb` in Google Colab
   - Or create a new Colab notebook and copy the cells

2. **Run the setup cell:**
   - Mount Google Drive
   - Set paths to your tourplanning_modules folder
   - Load required modules

3. **Load your VRP results:**
   - Either load from a saved JSON file
   - Or connect to your main TourPlanning_Script.ipynb

4. **Export tours for editing:**
   - Run the export cell
   - Download the CSV file

5. **Edit the CSV:**
   - Open in Excel/Google Sheets
   - Change the `Tour Stop Index` column to reorder stops
   - Lower numbers = earlier in tour

6. **Import edited tours:**
   - Upload the edited CSV
   - Run the import cell
   - Continue with your workflow

### Option 2: Integrate into Main Notebook

Add Step 5.5 to your `TourPlanning_Script.ipynb`:

```python
# Step 5.5: Tour Stop Order Editor
import sys
sys.path.insert(0, '/content/drive/MyDrive/Colab Notebooks/tourplanning_modules')
from tour_editor.module_tour_editor import export_tours_for_editing, import_tours_from_csv

# Export tours
export_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
export_tours_for_editing(vrp_response_json, df_geocoded, export_path)
```

## 📖 Usage Guide

### Exporting Tours

```python
from tour_editor.module_tour_editor import export_tours_for_editing

export_path = '/path/to/tours_for_editing.csv'
tour_df = export_tours_for_editing(
    vrp_response_json, 
    df_geocoded, 
    export_path
)
```

### Editing CSV

The exported CSV contains:
- `Tour Stop Index`: Change this to reorder (0 = first stop, 1 = second, etc.)
- `Job ID`: Order identifier
- `Activity Type`: pickup or delivery
- `Customer Name`, `Address`: For reference
- `Start Time`, `End Time`: Current times

**Important:**
- Lower `Tour Stop Index` = earlier in tour
- Keep activities with same stop index together
- Don't delete rows (only reorder)

### Importing Edited Tours

```python
from tour_editor.module_tour_editor import import_tours_from_csv

edited_csv_path = '/path/to/edited_tours.csv'
updated_vrp_response = import_tours_from_csv(
    edited_csv_path,
    vrp_response_json
)

# Update your variable
vrp_response_json = updated_vrp_response
```

## 🔧 Functions Reference

### `export_tours_for_editing()`
Exports all tours to CSV for editing.

**Parameters:**
- `vrp_response_json`: VRP response dictionary
- `df_geocoded`: Geocoded DataFrame with order details
- `output_path`: Path to save CSV file

**Returns:** DataFrame with tour data

### `import_tours_from_csv()`
Imports edited CSV and updates VRP response.

**Parameters:**
- `csv_path`: Path to edited CSV file
- `original_vrp_response`: Original VRP response

**Returns:** Updated VRP response dictionary

### `get_tour_stops_dataframe()`
Converts a tour's stops to DataFrame for viewing.

**Parameters:**
- `tour`: Tour dictionary
- `df_geocoded`: Geocoded DataFrame

**Returns:** DataFrame with stop information

### `create_simple_editor_interface()`
Displays current tour structure.

**Parameters:**
- `vrp_response_json`: VRP response
- `merged_df`: Merged DataFrame (optional)
- `df_geocoded`: Geocoded DataFrame

**Returns:** VRP response (unchanged, for display only)

## ⚠️ Important Notes

1. **Time Recalculation**: After reordering, activity times may be inaccurate. The module preserves original times but doesn't recalculate them automatically.

2. **Distance Updates**: Distances between stops may need manual adjustment.

3. **Validation**: Always verify:
   - All stops are present after import
   - Pickup comes before delivery (if required)
   - No duplicate stops

4. **Backup**: Always keep a backup of your original VRP response before editing.

## 🐛 Troubleshooting

### CSV Import Fails
- Check CSV format matches export format
- Ensure all required columns are present
- Verify `Tour Stop Index` values are integers

### Times Are Wrong After Import
- This is expected - times aren't recalculated automatically
- You may need to manually adjust or use HERE API to recalculate

### Can't Find Module
- Ensure `tour_editor` folder is in your Python path
- Check that `module_tour_editor.py` is in the folder

## 📚 Documentation

- **Design Document**: `docs/TOUR_EDITOR_DESIGN.md`
- **Summary**: `docs/TOUR_EDITOR_SUMMARY.md`
- **Integration Examples**: `docs/NOTEBOOK_INTEGRATION_EXAMPLE.md`

## 🔮 Future Enhancements

- Automatic time recalculation using HERE API
- Visual drag-and-drop editor
- Constraint validation
- Bulk operations
- Optimization suggestions

## 📝 Example Workflow

```python
# 1. After VRP execution, export tours
export_path = 'tours_for_editing.csv'
export_tours_for_editing(vrp_response_json, df_geocoded, export_path)

# 2. User edits CSV (changes Tour Stop Index)

# 3. Import edited tours
updated_vrp = import_tours_from_csv(export_path, vrp_response_json)

# 4. Use updated response
vrp_response_json = updated_vrp

# 5. Continue with results merging
merged_df, df_unassigned = merge_results(
    vrp_response_json, df_geocoded, output_folder_path, depots_path
)
```

## 💡 Tips

- Start with small tours to test the workflow
- Use Excel/Google Sheets for easier editing
- Keep original CSV as backup
- Test import before continuing with full workflow


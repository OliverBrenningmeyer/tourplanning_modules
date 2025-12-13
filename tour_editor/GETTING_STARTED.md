# Getting Started with Tour Editor

## 📁 Folder Structure

Your organized folder structure:

```
tourplanning_modules/
├── tour_editor/                          # Tour Editor Module
│   ├── __init__.py                       # Package initialization
│   ├── module_tour_editor.py             # Core module
│   ├── TourEditor_Standalone.ipynb      # Standalone Colab notebook ⭐
│   ├── README.md                         # Full documentation
│   ├── QUICK_START.md                    # Quick start guide
│   ├── GETTING_STARTED.md                # This file
│   └── docs/
│       ├── TOUR_EDITOR_DESIGN.md         # Design document
│       ├── TOUR_EDITOR_SUMMARY.md        # Summary
│       └── NOTEBOOK_INTEGRATION_EXAMPLE.md
│
├── module_*.py                           # Other modules
├── TourPlanning_Script.ipynb             # Main notebook
└── ...
```

## 🎯 Quick Start (3 Steps)

### 1. Open the Standalone Notebook

**In Google Colab:**
- Navigate to: `tour_editor/TourEditor_Standalone.ipynb`
- Or upload it to Colab from your Drive

### 2. Run the Cells

Follow the notebook step by step:
1. **Setup** - Mount Drive and set paths
2. **Load Data** - Load your VRP results
3. **Export** - Export tours to CSV
4. **Edit** - Edit CSV in Excel/Sheets
5. **Import** - Import edited CSV
6. **Continue** - Use updated tours

### 3. Edit and Import

- Download the exported CSV
- Edit `Tour Stop Index` column
- Upload back
- Import to update tours

## 📖 Detailed Steps

### Step 1: Setup

```python
# In TourEditor_Standalone.ipynb, Step 1:
module_path = '/content/drive/MyDrive/Colab Notebooks/tourplanning_modules'
# Update this to match your folder location
```

### Step 2: Load Your Data

**Option A - From Files:**
```python
# Update these paths:
vrp_response_file = '/path/to/vrp_response.json'
geocoded_file = '/path/to/geocoded_data.csv'
```

**Option B - From Variables:**
- If you just ran `TourPlanning_Script.ipynb`
- Variables are already in memory
- Just verify they exist

### Step 3: Export Tours

```python
# Set your date and client
base_date_str = "2025-12-15"
client_name = "Kemmler"

# Export
export_tours_for_editing(vrp_response_json, df_geocoded, export_path)
```

### Step 4: Edit CSV

1. Open CSV in Excel/Google Sheets
2. Find `Tour Stop Index` column
3. Change values to reorder:
   - `0` = first stop
   - `1` = second stop
   - etc.
4. Save file

### Step 5: Import

```python
# Upload edited CSV, then:
import_tours_from_csv(edited_csv_path, vrp_response_json)
# vrp_response_json is now updated!
```

## 🔗 Integration with Main Notebook

### Option 1: Standalone (Recommended)

1. Run `TourPlanning_Script.ipynb` through Step 5
2. Open `TourEditor_Standalone.ipynb`
3. Load data (Option B - from variables)
4. Edit tours
5. Continue in main notebook with updated `vrp_response_json`

### Option 2: Integrated Step

Add Step 5.5 to `TourPlanning_Script.ipynb`:

```python
# Step 5.5: Tour Editor
import sys
sys.path.insert(0, '/content/drive/MyDrive/Colab Notebooks/tourplanning_modules')
from tour_editor import export_tours_for_editing, import_tours_from_csv

# Export
export_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
export_tours_for_editing(vrp_response_json, df_geocoded, export_path)

# (User edits CSV manually)

# Import (after editing)
# import_tours_from_csv(export_path, vrp_response_json)
```

## 📝 Example Workflow

```
1. Run TourPlanning_Script.ipynb Steps 1-5
   └─> VRP optimization completes
   
2. Open TourEditor_Standalone.ipynb
   └─> Load data (Option B)
   └─> Export tours to CSV
   
3. Edit CSV in Excel
   └─> Change Tour Stop Index values
   └─> Save file
   
4. Back in TourEditor_Standalone.ipynb
   └─> Upload edited CSV
   └─> Import tours
   └─> vrp_response_json updated!
   
5. Continue in TourPlanning_Script.ipynb
   └─> Step 6: Results Merging (uses updated order)
   └─> Step 7: Export
   └─> Step 8: Visualization
```

## 🎨 CSV Editing Example

**Original Order:**
```
Tour Stop Index | Job ID | Activity Type | Customer
0               | 12345  | pickup       | Depot A
1               | 12345  | delivery     | Customer X
2               | 12346  | pickup       | Depot B
3               | 12346  | delivery     | Customer Y
```

**After Editing (Job 12346 first):**
```
Tour Stop Index | Job ID | Activity Type | Customer
0               | 12346  | pickup       | Depot B      ← Changed from 2
1               | 12346  | delivery     | Customer Y   ← Changed from 3
2               | 12345  | pickup       | Depot A      ← Changed from 0
3               | 12345  | delivery     | Customer X   ← Changed from 1
```

## ⚠️ Important Notes

1. **Times**: Activity times are preserved but not recalculated. They may be inaccurate after reordering.

2. **Distances**: Distances between stops may need manual adjustment.

3. **Validation**: Always verify:
   - All stops are present
   - Pickup before delivery (if required)
   - No duplicate stops

4. **Backup**: Keep a copy of original CSV before editing.

## 🐛 Common Issues

### "Module not found"
- Check `module_path` in Step 1
- Ensure `tour_editor` folder exists in `tourplanning_modules`

### "File not found"
- Verify file paths in Option A
- Check files exist in those locations

### "Import failed"
- CSV format must match export format
- All columns must be present
- Tour Stop Index must be integers

## 📚 Documentation

- **README.md** - Full documentation
- **QUICK_START.md** - 5-minute quick start
- **docs/TOUR_EDITOR_DESIGN.md** - Architecture details
- **docs/TOUR_EDITOR_SUMMARY.md** - Quick reference

## 🚀 Next Steps

1. ✅ Open `TourEditor_Standalone.ipynb`
2. ✅ Follow the steps
3. ✅ Export and edit your first tour
4. ✅ Import and see the results!

---

**Ready to start?** Open `TourEditor_Standalone.ipynb` in Google Colab! 🎉


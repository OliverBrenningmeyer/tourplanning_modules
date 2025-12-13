# Quick Start Guide - Tour Editor

## 🚀 Get Started in 5 Minutes

### Step 1: Open the Notebook

1. Go to Google Colab
2. Open `TourEditor_Standalone.ipynb` from your Drive
3. Or upload it to Colab

### Step 2: Run Setup

1. Run **Step 1: Setup and Mount Drive**
   - Update the `module_path` to your folder location
   - Mount your Google Drive

2. Run **Step 2: Import Required Modules**
   - This loads all necessary functions

### Step 3: Load Your Data

Choose one option:

**Option A - From Files:**
- Run **Option A: Load from JSON File**
- Update paths to your VRP response JSON and geocoded CSV

**Option B - From Variables:**
- If you just ran `TourPlanning_Script.ipynb`
- Run **Option B: Use Variables from Main Notebook**
- Variables should already be in memory

### Step 4: Export Tours

1. Run **Step 5: Export Tours to CSV**
2. Update `base_date_str` and `client_name` if needed
3. Download the CSV file from the output folder

### Step 5: Edit CSV

1. Open the CSV in Excel or Google Sheets
2. Find the `Tour Stop Index` column
3. Change the numbers to reorder stops:
   - `0` = first stop
   - `1` = second stop
   - `2` = third stop
   - etc.
4. Save the file

### Step 6: Import Edited Tours

1. Upload the edited CSV back to the same location
2. Run **Step 6: Import Edited CSV**
3. The `vrp_response_json` variable is now updated!

### Step 7: Continue Your Workflow

Use the updated `vrp_response_json` in your main notebook or continue with results merging.

## 📝 Example: Reordering a Tour

**Before (CSV):**
```
Tour Stop Index | Job ID | Activity Type
0               | 12345  | pickup
1               | 12345  | delivery
2               | 12346  | pickup
3               | 12346  | delivery
```

**After (edited CSV):**
```
Tour Stop Index | Job ID | Activity Type
0               | 12346  | pickup      ← Changed from 2 to 0
1               | 12346  | delivery    ← Changed from 3 to 1
2               | 12345  | pickup      ← Changed from 0 to 2
3               | 12345  | delivery    ← Changed from 1 to 3
```

Now Job 12346 will be visited before Job 12345!

## ⚠️ Important Tips

1. **Keep activities together**: If a job has both pickup and delivery, keep them close in order
2. **Don't delete rows**: Only change the `Tour Stop Index` values
3. **Use integers**: Tour Stop Index must be whole numbers (0, 1, 2, ...)
4. **Backup first**: Always keep a copy of the original CSV

## 🐛 Troubleshooting

**"Module not found" error:**
- Check that `module_path` in Step 1 points to your `tourplanning_modules` folder
- Make sure `tour_editor` folder is inside `tourplanning_modules`

**"File not found" error:**
- Check file paths in Option A
- Make sure files exist in those locations

**"Import failed" error:**
- Check CSV format matches export format
- Ensure all columns are present
- Verify Tour Stop Index values are integers

## 📚 Need More Help?

- See `README.md` for detailed documentation
- Check `docs/TOUR_EDITOR_DESIGN.md` for architecture details
- Review `docs/NOTEBOOK_INTEGRATION_EXAMPLE.md` for integration examples


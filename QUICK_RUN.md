# Quick Run Guide

## The Three Commands to Run Tour Planning Locally

### Step 1: Navigate to the directory
```bash
cd "/Users/oliverroscher/Library/CloudStorage/GoogleDrive-oliver.brenningmeyer@bexapp.de/Meine Ablage/Colab Notebooks/tourplanning_modules"
```

### Step 2: Set your API key
```bash
export HERE_API_KEY='your_api_key_here'
```

### Step 3: Run the script
```bash
python3 run_tour_planning_gdrive.py
```

---

## Running in Cursor IDE

Yes! You can run this directly in Cursor:

1. **Open the integrated terminal in Cursor:**
   - Press `` Ctrl+` `` (backtick) or `Cmd+` ` on Mac
   - Or go to: `Terminal → New Terminal`

2. **The terminal will automatically be in the project directory** (if you opened the `tourplanning_modules` folder)

3. **Run the commands:**
   ```bash
   export HERE_API_KEY='your_api_key_here'
   python3 run_tour_planning_gdrive.py
   ```

4. **You can also create a Cursor task** (see below)

---

## Alternative: One-Line Command

If you want to set the API key and run in one go:
```bash
export HERE_API_KEY='your_api_key_here' && python3 run_tour_planning_gdrive.py
```

---

## Using .env File (Recommended for Cursor)

Instead of exporting each time, create a `.env` file:

1. Create `.env` file in the project root:
   ```
   HERE_API_KEY=your_api_key_here
   ```

2. The script will automatically load it (if python-dotenv is installed)

3. Then just run:
   ```bash
   python3 run_tour_planning_gdrive.py
   ```

---

## Cursor Tasks (Advanced)

You can create a Cursor task to run this automatically:

1. Create `.cursor/tasks.json`:
   ```json
   {
     "tasks": [
       {
         "label": "Run Tour Planning",
         "type": "shell",
         "command": "python3 run_tour_planning_gdrive.py",
         "problemMatcher": []
       }
     ]
   }
   ```

2. Then run it via: `Cmd+Shift+P` → "Tasks: Run Task" → "Run Tour Planning"

---

## Quick Reference

**Location:** `/Users/oliverroscher/Library/CloudStorage/GoogleDrive-oliver.brenningmeyer@bexapp.de/Meine Ablage/Colab Notebooks/tourplanning_modules`

**Script:** `run_tour_planning_gdrive.py` (uses Google Drive files directly)

**Alternative:** `run_tour_planning.py` (uses local `data/` folder)

---

## Troubleshooting

**If API key not found:**
- Make sure you exported it: `export HERE_API_KEY='your_key'`
- Or create `.env` file with the key

**If module not found:**
- Make sure you're in the `tourplanning_modules` directory
- Check: `ls run_tour_planning_gdrive.py` should show the file

**If file not found:**
- Check Google Drive is synced
- Verify input file exists at the expected path


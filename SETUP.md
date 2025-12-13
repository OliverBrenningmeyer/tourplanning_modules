# GitHub Repository Setup Guide

This guide helps you set up this repository on GitHub and ensure it works correctly in Google Colab.

## Files Included in Repository

The following files are tracked in Git:

### Core Modules
- `module_upload.py` - File upload handling
- `module_clean.py` - Data cleaning and preprocessing
- `module_column_mapping.py` - Column name mappings
- `module_geocoding.py` - Address geocoding
- `module_vrp.py` - VRP problem definition and execution
- `module_results.py` - Results merging and processing
- `module_export.py` - Export file generation
- `module_map.py` - Map visualization
- `module_client_configuration.py` - Client configurations

### Configuration Files
- `__init__.py` - Package initialization
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `.gitignore` - Git ignore rules
- `SETUP.md` - This file

### Notebooks
- `TourPlanning_Script.ipynb` - Main execution notebook

## Files Excluded from Repository

The following are excluded via `.gitignore`:
- `venv/` - Virtual environment (not needed in Colab)
- `__pycache__/` - Python cache files
- `Kemmler_Export_File_With_TrackingLinks.ipynb` - Client-specific notebook
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

## Setting Up the Repository

### 1. Initialize Git Repository

```bash
cd tourplanning_modules
git init
git add .
git commit -m "Initial commit: Tour planning modules"
```

### 2. Create GitHub Repository

1. Go to GitHub and create a new repository
2. **Do not** initialize with README, .gitignore, or license (we already have these)
3. Copy the repository URL

### 3. Connect and Push

```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## Google Colab Setup

### 1. Upload to Google Drive

After cloning or downloading from GitHub:

1. Upload the entire `tourplanning_modules` folder to:
   ```
   MyDrive/Colab Notebooks/tourplanning_modules/
   ```

2. Ensure your folder structure matches:
   ```
   MyDrive/Colab Notebooks/
   ├── tourplanning_modules/          # This repository
   │   ├── module_*.py
   │   ├── TourPlanning_Script.ipynb
   │   └── ...
   ├── {client_name}/                 # Your client data folders
   │   ├── depots/
   │   │   └── Depots_geocoded.xlsx
   │   └── {date}/                    # Output (auto-created)
   ```

### 2. Open in Colab

1. Navigate to the folder in Google Drive
2. Right-click `TourPlanning_Script.ipynb`
3. Select "Open with" → "Google Colaboratory"

### 3. Configure API Key

1. In Colab, go to the key icon (🔑) in the left sidebar
2. Click "Add new secret"
3. Name: `apiKey_HERE`
4. Value: Your HERE API key
5. Click "Add secret"

### 4. Run the Notebook

1. Execute cells sequentially
2. The notebook will:
   - Mount Google Drive automatically
   - Load all modules from the repository
   - Set up paths based on client selection

## Verifying Setup

After setup, verify:

- ✅ All module files are in `MyDrive/Colab Notebooks/tourplanning_modules/`
- ✅ Client data folders exist with depot files
- ✅ HERE API key is stored in Colab secrets
- ✅ Notebook can import all modules without errors
- ✅ Paths in notebook match your Google Drive structure

## Updating the Repository

When making changes:

1. **Test in Colab first** - Ensure changes work before committing
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. **Update Google Drive** - Pull or re-upload updated files to Drive

## Troubleshooting

### Module Import Errors

If modules can't be imported:
- Check that the module path in the notebook matches your Drive structure
- Verify all `.py` files are in the `tourplanning_modules` folder
- Restart the Colab runtime and re-run the first cell

### Path Errors

If paths don't work:
- **Do not modify paths in the notebook** - they are designed for the specific structure
- Ensure your Google Drive folder structure matches the expected layout
- Check that client names match exactly (case-sensitive)

### API Errors

If HERE API calls fail:
- Verify your API key is correct in Colab secrets
- Check API key has necessary permissions (Geocoding + Tour Planning)
- Verify you haven't exceeded rate limits

## Repository Maintenance

### Adding New Clients

1. Add column mapping in `module_column_mapping.py`
2. Add configuration in `module_client_configuration.py`
3. Update client selection in `TourPlanning_Script.ipynb`
4. Test thoroughly before committing

### Updating Dependencies

1. Update `requirements.txt`
2. Test in Colab
3. Commit and push changes

### Documentation Updates

- Keep `README.md` updated with new features
- Update this file if setup process changes
- Document any breaking changes


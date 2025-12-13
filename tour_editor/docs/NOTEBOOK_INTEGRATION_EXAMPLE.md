# Notebook Integration Example

## How to Add Tour Editor to TourPlanning_Script.ipynb

### Step 1: Add the new cell after Step 5 (VRP Execution)

Insert this cell between Step 5 and Step 6:

```python
# @title Step 5.5: Tour Stop Order Editor (Optional)

print("="*80)
print("STEP 5.5: TOUR STOP ORDER EDITOR")
print("="*80)
print("This step allows you to reorder stops within tours.")
print("You can skip this step if you're satisfied with the VRP-optimized order.")
print()

# Ask user if they want to edit tours
edit_tours = True  # @param {type:"boolean"} Set to False to skip editing

if edit_tours:
    try:
        # Import the tour editor module
        import module_tour_editor
        
        # Display current tour structure
        print("Current Tour Structure:")
        print("-"*80)
        updated_vrp_response = module_tour_editor.create_simple_editor_interface(
            vrp_response_json, 
            merged_df if 'merged_df' in locals() else None,  # May not exist yet
            df_geocoded
        )
        
        # Option 1: Export for manual editing
        export_for_editing = True  # @param {type:"boolean"}
        
        if export_for_editing:
            export_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
            tour_export_df = module_tour_editor.export_tours_for_editing(
                vrp_response_json, 
                df_geocoded, 
                export_path
            )
            
            print("\n" + "="*80)
            print("EDITING INSTRUCTIONS:")
            print("="*80)
            print("1. Download the CSV file from:", export_path)
            print("2. Open it in Excel or Google Sheets")
            print("3. Edit the 'Tour Stop Index' column to change stop order")
            print("   - Lower numbers = earlier in tour")
            print("   - Keep activities with same stop index together")
            print("4. Save the file")
            print("5. Upload it back to the same location")
            print("6. Run the import cell below")
            print("="*80)
            
            # Option to import after editing
            import_edited = False  # @param {type:"boolean"} Set to True after editing CSV
            
            if import_edited:
                try:
                    updated_vrp_response = module_tour_editor.import_tours_from_csv(
                        export_path,
                        vrp_response_json
                    )
                    
                    # Update the vrp_response_json variable
                    vrp_response_json = updated_vrp_response
                    
                    tracker.add_step("Tour Editing", "success", 
                                    "Tour stop order updated from CSV",
                                    {"export_path": export_path})
                    
                    print("\n✅ Tour order updated successfully!")
                    print("   Continuing with updated tour order...")
                    
                except Exception as e:
                    tracker.add_step("Tour Editing", "error", 
                                    f"Failed to import edited tours: {str(e)}",
                                    {"hint": "Check CSV format and file path"})
                    print(f"\n❌ Error importing edited tours: {str(e)}")
                    print("   Continuing with original tour order...")
            else:
                print("\n⚠️  Skipping import. Using original tour order.")
                print("   Set 'import_edited' to True after editing the CSV file.")
        else:
            print("\n⚠️  Tour editing skipped. Using original VRP-optimized order.")
        
        print("="*80)
        
    except Exception as e:
        tracker.add_step("Tour Editing", "error", 
                        f"Tour editor failed: {str(e)}",
                        {"hint": "Check that module_tour_editor is available"})
        print(f"⚠️  Tour editor error: {str(e)}")
        print("   Continuing with original tour order...")
else:
    print("Tour editing skipped. Using original VRP-optimized order.")
    tracker.add_step("Tour Editing", "skipped", "Tour editing was skipped by user")
    print("="*80)
```

### Step 2: Alternative - Interactive Widget Version

If you want to use interactive widgets (may not work in all Colab environments):

```python
# @title Step 5.5: Interactive Tour Editor (Alternative)

print("="*80)
print("STEP 5.5: INTERACTIVE TOUR EDITOR")
print("="*80)

try:
    import module_tour_editor
    
    # Try interactive editor
    updated_vrp_response = module_tour_editor.create_interactive_editor_colab(
        vrp_response_json,
        merged_df if 'merged_df' in locals() else None,
        df_geocoded
    )
    
    # If user made changes, update vrp_response_json
    # (This would need additional logic to capture widget changes)
    
    tracker.add_step("Tour Editing", "success", "Interactive tour editor displayed")
    
except Exception as e:
    print(f"⚠️  Interactive editor not available: {str(e)}")
    print("   Falling back to export/import method...")
    
    # Fallback to export/import
    export_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
    module_tour_editor.export_tours_for_editing(
        vrp_response_json, df_geocoded, export_path
    )
    
    print("="*80)
```

### Step 3: Simplified Version (Recommended for First Implementation)

For the simplest integration, use this minimal version:

```python
# @title Step 5.5: View and Export Tours for Editing

print("="*80)
print("STEP 5.5: TOUR EDITOR")
print("="*80)

try:
    import module_tour_editor
    
    # Display tours
    print("Current Tours:")
    print("-"*80)
    for idx, tour in enumerate(vrp_response_json.get('tours', [])):
        vehicle_id = tour.get('vehicleId', 'Unknown')
        num_stops = len([s for s in tour.get('stops', []) if s.get('activities')])
        print(f"Tour {idx + 1}: Vehicle {vehicle_id} - {num_stops} stops")
    
    print()
    
    # Export option
    export_tours = True  # @param {type:"boolean"}
    
    if export_tours:
        export_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
        tour_df = module_tour_editor.export_tours_for_editing(
            vrp_response_json,
            df_geocoded,
            export_path
        )
        
        print("\n📝 To edit tour order:")
        print("   1. Download the CSV file")
        print("   2. Edit 'Tour Stop Index' column (lower = earlier)")
        print("   3. Upload back and run import cell")
        
        tracker.add_step("Tour Export", "success", 
                        f"Tours exported for editing: {export_path}")
    else:
        print("Tour export skipped.")
    
    print("="*80)
    
except Exception as e:
    tracker.add_step("Tour Editor", "error", f"Tour editor failed: {str(e)}")
    print(f"⚠️  Error: {str(e)}")
    print("="*80)
```

### Step 4: Import Cell (Run after editing CSV)

Add this cell that users can run after editing the CSV:

```python
# @title Import Edited Tours

print("="*80)
print("IMPORT EDITED TOURS")
print("="*80)

try:
    import module_tour_editor
    
    # Path to edited CSV
    edited_csv_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
    
    # Import and update
    updated_vrp_response = module_tour_editor.import_tours_from_csv(
        edited_csv_path,
        vrp_response_json
    )
    
    # Update the main variable
    vrp_response_json = updated_vrp_response
    
    print("\n✅ Tours imported successfully!")
    print("   Tour order has been updated.")
    print("   Continue with Step 6 to see updated results.")
    
    tracker.add_step("Tour Import", "success", 
                    "Edited tours imported successfully",
                    {"path": edited_csv_path})
    
except FileNotFoundError:
    print(f"❌ File not found: {edited_csv_path}")
    print("   Make sure you've uploaded the edited CSV file.")
    tracker.add_step("Tour Import", "error", "CSV file not found")
    
except Exception as e:
    print(f"❌ Error importing tours: {str(e)}")
    tracker.add_step("Tour Import", "error", f"Import failed: {str(e)}")

print("="*80)
```

## Integration Checklist

- [ ] Add `module_tour_editor.py` to the tourplanning_modules folder
- [ ] Insert Step 5.5 cell after Step 5 in the notebook
- [ ] Add import cell for edited tours (optional, can be separate)
- [ ] Test with sample data
- [ ] Update documentation
- [ ] Add error handling for edge cases

## Usage Flow

1. **Run Steps 1-5** as normal
2. **Run Step 5.5** to view/export tours
3. **Edit CSV** (if needed) - change Tour Stop Index values
4. **Run Import cell** (if edited)
5. **Continue with Steps 6-8** - results will use updated order

## Notes

- The editor is **optional** - users can skip it
- Original VRP order is preserved if no editing occurs
- CSV export/import is the most reliable method for Colab
- Times and distances may need manual adjustment after reordering


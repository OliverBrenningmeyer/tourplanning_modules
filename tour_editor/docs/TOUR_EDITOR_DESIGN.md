# Tour Stop Order Editor - Design Document

## Overview
This document describes the design for allowing users to change stop order within tours as part of the TourPlanning_Script.ipynb workflow.

## Architecture

### Components

1. **module_tour_editor.py** - Core module with editing functions
2. **New Notebook Step** - Interactive editing step between VRP execution and results merging
3. **Export/Import Workflow** - CSV-based editing for complex reordering

### Data Flow

```
VRP Execution (Step 5)
    ↓
Tour Editor (NEW Step 5.5)
    ↓
Updated VRP Response
    ↓
Results Merging (Step 6)
    ↓
Export & Visualization (Steps 7-8)
```

## Implementation Options

### Option 1: Simple Display + Export/Import (Recommended for Colab)
- **Pros**: Works reliably in Colab, no complex dependencies
- **Cons**: Requires manual CSV editing
- **Use Case**: When users need to make occasional adjustments

**Workflow:**
1. Display current tour structure
2. Export tours to CSV
3. User edits CSV (changes stop indices)
4. Import edited CSV
5. Continue with updated order

### Option 2: Interactive Widgets (Advanced)
- **Pros**: More user-friendly, visual interface
- **Cons**: May have compatibility issues in Colab
- **Use Case**: When frequent editing is needed

**Workflow:**
1. Display tour selector dropdown
2. Show stops in editable table
3. Drag-and-drop or manual reordering
4. Apply changes immediately

### Option 3: Hybrid Approach (Best of Both)
- **Pros**: Flexible, works in all environments
- **Cons**: More complex implementation
- **Use Case**: Production-ready solution

**Workflow:**
1. Display tours with interactive widgets (if available)
2. Fallback to export/import if widgets fail
3. Support both methods

## Integration Points

### Location in Notebook
Insert new step between:
- **Step 5**: VRP Execution
- **Step 6**: Results Merging

### Code Integration

```python
# Step 5.5: Tour Stop Order Editor (NEW)
print("="*80)
print("STEP 5.5: TOUR STOP ORDER EDITOR")
print("="*80)

# Option 1: Simple interface
updated_vrp_response = module_tour_editor.create_simple_editor_interface(
    vrp_response_json, merged_df, df_geocoded
)

# Option 2: Export for editing
export_path = output_folder_path + '/' + base_date_str + '_tours_for_editing.csv'
module_tour_editor.export_tours_for_editing(
    vrp_response_json, df_geocoded, export_path
)

# User edits CSV manually, then:
# updated_vrp_response = module_tour_editor.import_tours_from_csv(
#     export_path, vrp_response_json
# )

# Update the vrp_response_json variable
vrp_response_json = updated_vrp_response
```

## Data Structure Considerations

### VRP Response Structure
```json
{
  "tours": [
    {
      "vehicleId": "vehicle_1",
      "typeId": "type_1",
      "stops": [
        {
          "activities": [
            {
              "jobId": "job_123",
              "type": "pickup",
              "location": {...},
              "time": {...}
            }
          ],
          "distance": 1000
        }
      ],
      "statistic": {...}
    }
  ]
}
```

### After Reordering
- **Stops array**: Reordered
- **Times**: Need recalculation (or manual update)
- **Distances**: Need recalculation (or manual update)
- **Statistics**: Need recalculation

### Important Notes
1. **Time Recalculation**: After reordering, activity times should be recalculated based on:
   - Travel time between stops
   - Service duration at each stop
   - Time windows

2. **Distance Recalculation**: Distances between stops need updating

3. **Validation**: Ensure:
   - All stops remain in the tour
   - No duplicate stops
   - Pickup before delivery (if required)

## User Interface Design

### Simple Interface
```
============================================================
TOUR STOP ORDER EDITOR
============================================================

Available Tours:
------------------------------------------------------------
1. Vehicle: vehicle_1 | Type: type_1 | Stops: 5
2. Vehicle: vehicle_2 | Type: type_2 | Stops: 3

============================================================
TOUR 1: Vehicle vehicle_1
============================================================

Stop Order (Current):
------------------------------------------------------------
  1. [pickup  ] Job 12345     | Customer Name          | 08:00:00
  2. [delivery] Job 12345     | Delivery Address       | 09:30:00
  3. [pickup  ] Job 12346     | Another Customer       | 10:15:00
  ...

Export Options:
- Export to CSV for editing
- Import from CSV after editing
```

### Interactive Interface (if widgets available)
- Dropdown: Select tour
- Table: Display stops with drag-and-drop
- Buttons: Move up/down, Apply changes

## Export/Import Format

### CSV Structure
```csv
Vehicle ID,Type ID,Tour Stop Index,Activity Index,Job ID,Activity Type,Start Time,End Time,Latitude,Longitude,Customer Name,Address,City
vehicle_1,type_1,0,0,12345,pickup,08:00:00,08:15:00,52.5,13.4,Customer A,Address A,City A
vehicle_1,type_1,1,0,12345,delivery,09:30:00,09:45:00,52.6,13.5,Customer B,Address B,City B
```

### Editing Instructions
1. Change `Tour Stop Index` to reorder stops
2. Lower index = earlier in tour
3. Keep `Activity Index` for activities at same location
4. Save and re-import

## Error Handling

### Validation Checks
1. **Stop Count**: Ensure all stops are present after import
2. **Job IDs**: Verify all job IDs exist
3. **Activity Types**: Validate pickup/delivery pairs
4. **Time Windows**: Check if new order violates time windows

### Error Messages
- "Missing stops detected after import"
- "Invalid job ID found"
- "Pickup must come before delivery for job X"

## Future Enhancements

1. **Automatic Time Recalculation**: Use HERE API to recalculate times
2. **Visual Drag-and-Drop**: Interactive map-based editor
3. **Constraint Validation**: Check time windows, capacity, etc.
4. **Undo/Redo**: Track changes for easy reversal
5. **Bulk Operations**: Move multiple stops at once
6. **Optimization Suggestions**: Suggest better orders

## Testing Considerations

1. **Test Cases**:
   - Reorder stops in single tour
   - Reorder stops in multiple tours
   - Import malformed CSV
   - Reorder with time window constraints

2. **Edge Cases**:
   - Empty tours
   - Tours with single stop
   - Very long tours (100+ stops)

## Performance Considerations

- **Large Tours**: For tours with 50+ stops, consider pagination
- **Multiple Tours**: Process one tour at a time
- **CSV Size**: Limit export to active tours only


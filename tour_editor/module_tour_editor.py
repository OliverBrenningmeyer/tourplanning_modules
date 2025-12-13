"""
Tour Editor Module - Allows users to reorder stops within tours
"""

import pandas as pd
import json
from typing import Dict, List, Optional
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from datetime import datetime, timedelta


def display_tour_editor(vrp_response_json: dict, merged_df: pd.DataFrame, 
                       df_geocoded: pd.DataFrame) -> dict:
    """
    Display an interactive interface for editing tour stop orders.
    
    Args:
        vrp_response_json: The VRP response JSON with tours
        merged_df: Merged DataFrame with tour activities
        df_geocoded: Geocoded DataFrame with order details
        
    Returns:
        Updated vrp_response_json with reordered stops
    """
    print("=" * 80)
    print("TOUR STOP ORDER EDITOR")
    print("=" * 80)
    print("You can reorder stops within each tour.")
    print("Changes will be applied to the tour planning results.")
    print()
    
    # Create a copy to avoid modifying the original
    updated_vrp_response = json.loads(json.dumps(vrp_response_json))
    
    tours = updated_vrp_response.get('tours', [])
    if not tours:
        print("⚠️  No tours available to edit.")
        return updated_vrp_response
    
    # Display tours for selection
    print("Available Tours:")
    print("-" * 80)
    for idx, tour in enumerate(tours):
        vehicle_id = tour.get('vehicleId', 'Unknown')
        type_id = tour.get('typeId', 'Unknown')
        num_stops = len([s for s in tour.get('stops', []) if s.get('activities')])
        print(f"{idx + 1}. Vehicle: {vehicle_id} | Type: {type_id} | Stops: {num_stops}")
    print()
    
    # For Colab, we'll use a simpler interface
    # In a real implementation, you might want to use ipywidgets for interactivity
    print("=" * 80)
    print("TOUR EDITING INTERFACE")
    print("=" * 80)
    print("Note: This is a simplified interface. For full editing capabilities,")
    print("you can export the tour data, edit it, and re-import.")
    print()
    
    return updated_vrp_response


def get_tour_stops_dataframe(tour: dict, df_geocoded: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a tour's stops into a DataFrame for easy editing.
    
    Args:
        tour: Tour dictionary from VRP response
        df_geocoded: Geocoded DataFrame with order details
        
    Returns:
        DataFrame with stop information
    """
    stops_data = []
    
    for stop_idx, stop in enumerate(tour.get('stops', [])):
        for activity_idx, activity in enumerate(stop.get('activities', [])):
            job_id = activity.get('jobId')
            activity_type = activity.get('type')
            
            # Get order details from geocoded data
            order_info = df_geocoded[df_geocoded['Auftr.-Nr.'] == job_id]
            
            customer_name = 'N/A'
            address = 'N/A'
            if not order_info.empty:
                row = order_info.iloc[0]
                if activity_type == 'delivery':
                    customer_name = row.get('Empfänger', 'N/A')
                    address = row.get('dropoff_label', 'N/A')
                elif activity_type == 'pickup':
                    customer_name = row.get('Vers.-Name', 'N/A')
                    address = row.get('pickup_label', 'N/A')
            
            stops_data.append({
                'Stop Index': stop_idx,
                'Activity Index': activity_idx,
                'Job ID': job_id,
                'Activity Type': activity_type,
                'Customer': customer_name,
                'Address': address,
                'Start Time': activity.get('time', {}).get('start', 'N/A'),
                'End Time': activity.get('time', {}).get('end', 'N/A'),
                'Latitude': activity.get('location', {}).get('lat', 0),
                'Longitude': activity.get('location', {}).get('lng', 0),
            })
    
    return pd.DataFrame(stops_data)


def reorder_tour_stops(vrp_response_json: dict, vehicle_id: str, 
                      new_stop_order: List[Dict]) -> dict:
    """
    Reorder stops within a specific tour.
    
    Args:
        vrp_response_json: The VRP response JSON
        vehicle_id: Vehicle ID of the tour to modify
        new_stop_order: List of stop dictionaries in the new order
        
    Returns:
        Updated vrp_response_json
    """
    updated_vrp_response = json.loads(json.dumps(vrp_response_json))
    
    # Find the tour
    for tour in updated_vrp_response.get('tours', []):
        if tour.get('vehicleId') == vehicle_id:
            # Replace stops with new order
            tour['stops'] = new_stop_order
            
            # Note: After reordering, times and distances would need to be recalculated
            # This is a simplified version - in production, you'd want to:
            # 1. Recalculate travel times between stops
            # 2. Update activity start/end times
            # 3. Update tour statistics
            
            break
    
    return updated_vrp_response


def create_simple_editor_interface(vrp_response_json: dict, merged_df: pd.DataFrame,
                                   df_geocoded: pd.DataFrame) -> dict:
    """
    Create a simple text-based interface for editing tour orders.
    This works well in Colab where advanced widgets may not be available.
    
    Args:
        vrp_response_json: The VRP response JSON
        merged_df: Merged DataFrame with tour activities
        df_geocoded: Geocoded DataFrame with order details
        
    Returns:
        Updated vrp_response_json
    """
    updated_vrp_response = json.loads(json.dumps(vrp_response_json))
    tours = updated_vrp_response.get('tours', [])
    
    if not tours:
        print("⚠️  No tours to edit.")
        return updated_vrp_response
    
    print("=" * 80)
    print("SIMPLE TOUR EDITOR")
    print("=" * 80)
    print("This interface allows you to view and understand tour structure.")
    print("For manual editing, you can:")
    print("1. Export tour data to CSV")
    print("2. Edit the order")
    print("3. Re-import using the import function")
    print()
    
    # Display each tour's stops
    for tour_idx, tour in enumerate(tours):
        vehicle_id = tour.get('vehicleId', f'Tour_{tour_idx}')
        print(f"\n{'=' * 80}")
        print(f"TOUR {tour_idx + 1}: Vehicle {vehicle_id}")
        print(f"{'=' * 80}")
        
        stops_df = get_tour_stops_dataframe(tour, df_geocoded)
        
        if not stops_df.empty:
            # Display in a readable format
            print(f"\nStop Order (Current):")
            print("-" * 80)
            for idx, row in stops_df.iterrows():
                print(f"{idx + 1:3d}. [{row['Activity Type']:8s}] Job {row['Job ID']:10s} | "
                      f"{row['Customer'][:30]:30s} | {row['Start Time']}")
        else:
            print("No stops found in this tour.")
    
    print("\n" + "=" * 80)
    print("To reorder stops, use the advanced editor function or export/import workflow.")
    print("=" * 80)
    
    return updated_vrp_response


def export_tours_for_editing(vrp_response_json: dict, df_geocoded: pd.DataFrame,
                             output_path: str) -> pd.DataFrame:
    """
    Export tour data to CSV for external editing.
    
    Args:
        vrp_response_json: The VRP response JSON
        df_geocoded: Geocoded DataFrame with order details
        output_path: Path to save the CSV file
        
    Returns:
        DataFrame with tour stop data
    """
    all_tour_data = []
    
    for tour in vrp_response_json.get('tours', []):
        vehicle_id = tour.get('vehicleId', 'Unknown')
        type_id = tour.get('typeId', 'Unknown')
        
        for stop_idx, stop in enumerate(tour.get('stops', [])):
            for activity_idx, activity in enumerate(stop.get('activities', [])):
                job_id = activity.get('jobId')
                activity_type = activity.get('type')
                
                # Get order details
                order_info = df_geocoded[df_geocoded['Auftr.-Nr.'] == job_id]
                
                row_data = {
                    'Vehicle ID': vehicle_id,
                    'Type ID': type_id,
                    'Tour Stop Index': stop_idx,
                    'Activity Index': activity_idx,
                    'Job ID': job_id,
                    'Activity Type': activity_type,
                    'Start Time': activity.get('time', {}).get('start', ''),
                    'End Time': activity.get('time', {}).get('end', ''),
                    'Latitude': activity.get('location', {}).get('lat', 0),
                    'Longitude': activity.get('location', {}).get('lng', 0),
                }
                
                if not order_info.empty:
                    row = order_info.iloc[0]
                    row_data.update({
                        'Customer Name': row.get('Empfänger', '') if activity_type == 'delivery' else row.get('Vers.-Name', ''),
                        'Address': row.get('dropoff_label', '') if activity_type == 'delivery' else row.get('pickup_label', ''),
                        'City': row.get('dropoff_city', '') if activity_type == 'delivery' else row.get('pickup_city', ''),
                    })
                
                all_tour_data.append(row_data)
    
    tour_df = pd.DataFrame(all_tour_data)
    
    # Save to CSV
    if output_path:
        tour_df.to_csv(output_path, index=False)
        print(f"✅ Tour data exported to: {output_path}")
        print(f"   Total stops: {len(tour_df)}")
        print(f"   Edit the 'Tour Stop Index' column to change order")
        print(f"   Then use import_tours_from_csv() to reload")
    
    return tour_df


def import_tours_from_csv(csv_path: str, original_vrp_response: dict) -> dict:
    """
    Import tour data from CSV and update VRP response.
    
    Args:
        csv_path: Path to the edited CSV file
        original_vrp_response: Original VRP response to use as template
        
    Returns:
        Updated vrp_response_json with new stop order
    """
    # Read the edited CSV
    edited_df = pd.read_csv(csv_path)
    
    # Create updated VRP response
    updated_vrp_response = json.loads(json.dumps(original_vrp_response))
    
    # Group by vehicle
    for vehicle_id, vehicle_group in edited_df.groupby('Vehicle ID'):
        # Find the tour
        for tour in updated_vrp_response.get('tours', []):
            if tour.get('vehicleId') == vehicle_id:
                # Sort by new stop index
                vehicle_group = vehicle_group.sort_values('Tour Stop Index')
                
                # Rebuild stops
                new_stops = []
                current_stop_idx = None
                current_stop = None
                
                for _, row in vehicle_group.iterrows():
                    stop_idx = int(row['Tour Stop Index'])
                    
                    # Create activity
                    activity = {
                        'jobId': str(row['Job ID']),
                        'type': row['Activity Type'],
                        'location': {
                            'lat': float(row['Latitude']),
                            'lng': float(row['Longitude'])
                        },
                        'time': {
                            'start': row['Start Time'],
                            'end': row['End Time']
                        }
                    }
                    
                    # If new stop index, create new stop
                    if stop_idx != current_stop_idx:
                        if current_stop is not None:
                            new_stops.append(current_stop)
                        
                        current_stop = {
                            'activities': [activity],
                            'distance': 0  # Would need recalculation
                        }
                        current_stop_idx = stop_idx
                    else:
                        # Add to current stop
                        current_stop['activities'].append(activity)
                
                # Add last stop
                if current_stop is not None:
                    new_stops.append(current_stop)
                
                # Update tour
                tour['stops'] = new_stops
                
                # Note: Statistics would need recalculation
                break
    
    print(f"✅ Tour data imported from: {csv_path}")
    print("⚠️  Note: Times and distances may need recalculation")
    
    return updated_vrp_response


def create_interactive_editor_colab(vrp_response_json: dict, merged_df: pd.DataFrame,
                                    df_geocoded: pd.DataFrame) -> dict:
    """
    Create an interactive editor using Colab-compatible widgets.
    
    Args:
        vrp_response_json: The VRP response JSON
        merged_df: Merged DataFrame with tour activities
        df_geocoded: Geocoded DataFrame with order details
        
    Returns:
        Updated vrp_response_json
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display, clear_output
    except ImportError:
        print("⚠️  ipywidgets not available, using simple interface")
        return create_simple_editor_interface(vrp_response_json, merged_df, df_geocoded)
    
    updated_vrp_response = json.loads(json.dumps(vrp_response_json))
    tours = updated_vrp_response.get('tours', [])
    
    if not tours:
        print("⚠️  No tours to edit.")
        return updated_vrp_response
    
    # Create tour selector
    tour_options = [(f"Vehicle {t.get('vehicleId', i)} ({len(t.get('stops', []))} stops)", i) 
                    for i, t in enumerate(tours)]
    
    tour_selector = widgets.Dropdown(
        options=tour_options,
        description='Select Tour:',
        style={'description_width': 'initial'}
    )
    
    output = widgets.Output()
    
    def on_tour_change(change):
        with output:
            clear_output()
            tour_idx = change['new']
            tour = tours[tour_idx]
            vehicle_id = tour.get('vehicleId')
            
            print(f"Tour: {vehicle_id}")
            print("=" * 80)
            
            stops_df = get_tour_stops_dataframe(tour, df_geocoded)
            display(stops_df)
            
            print("\nTo reorder stops:")
            print("1. Export this tour using export_tours_for_editing()")
            print("2. Edit the CSV file")
            print("3. Import using import_tours_from_csv()")
    
    tour_selector.observe(on_tour_change, names='value')
    
    # Initial display
    with output:
        print("Select a tour from the dropdown above to view its stops.")
    
    display(tour_selector, output)
    
    return updated_vrp_response


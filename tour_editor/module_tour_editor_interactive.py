"""
Interactive Tour Editor with Visual Map Interface
Allows drag-and-drop reordering of stops with real-time map updates
"""

import pandas as pd
import json
import folium
from typing import Dict, List, Optional
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from datetime import datetime
import math


def create_interactive_tour_editor(vrp_response_json: dict, df_geocoded: pd.DataFrame, 
                                   merged_df: Optional[pd.DataFrame] = None) -> dict:
    """
    Create an interactive tour editor with map visualization and sortable stop list.
    
    Args:
        vrp_response_json: VRP response with tours
        df_geocoded: Geocoded DataFrame with order details
        merged_df: Optional merged DataFrame (will be created if not provided)
        
    Returns:
        Updated vrp_response_json with reordered stops
    """
    # Create merged_df if not provided
    if merged_df is None:
        merged_df = _create_merged_df_from_vrp(vrp_response_json, df_geocoded)
    
    tours = vrp_response_json.get('tours', [])
    if not tours:
        print("⚠️  No tours available to edit.")
        return vrp_response_json
    
    # Create a copy to avoid modifying original
    updated_vrp_response = json.loads(json.dumps(vrp_response_json))
    
    # Create main UI
    print("=" * 80)
    print("INTERACTIVE TOUR EDITOR")
    print("=" * 80)
    print("Select a tour to edit its stop order visually.")
    print()
    
    # Tour selector
    tour_options = [
        (f"Vehicle {t.get('vehicleId', i)} ({len([s for s in t.get('stops', []) if s.get('activities')])} stops)", i) 
        for i, t in enumerate(tours)
    ]
    
    tour_selector = widgets.Dropdown(
        options=tour_options,
        description='Select Tour:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='400px')
    )
    
    # Create output areas
    map_output = widgets.Output(layout=widgets.Layout(width='100%', height='600px'))
    stops_output = widgets.Output(layout=widgets.Layout(width='100%', height='500px'))
    control_output = widgets.Output()
    
    # Store current tour data (use a list to make it mutable in nested functions)
    current_tour_data = [{'tour_idx': 0, 'tour_df': None, 'vehicle_id': None}]
    
    def update_tour_display(tour_idx):
        """Update map and stops list for selected tour"""
        with map_output:
            clear_output(wait=True)
            
        with stops_output:
            clear_output(wait=True)
        
        tour = tours[tour_idx]
        vehicle_id = tour.get('vehicleId')
        
        # Get tour data
        tour_df = merged_df[merged_df['Vehicle ID'] == vehicle_id].copy()
        
        if tour_df.empty:
            with stops_output:
                print("No stops found for this tour.")
            return
        
        # Sort by current order (preserve VRP order based on stops sequence)
        # Reconstruct order from VRP stops
        stop_order = []
        for stop in tour.get('stops', []):
            for activity in stop.get('activities', []):
                job_id = activity.get('jobId')
                activity_type = activity.get('type')
                stop_order.append((job_id, activity_type))
        
        # Create order mapping
        order_map = {val: idx for idx, val in enumerate(stop_order)}
        tour_df['order'] = tour_df.apply(
            lambda row: order_map.get((str(row['Job ID']), row['Activity Type']), 999), axis=1
        )
        tour_df = tour_df.sort_values('order').reset_index(drop=True)
        tour_df = tour_df.drop('order', axis=1)
        
        # Store current tour data
        current_tour_data[0]['tour_df'] = tour_df
        current_tour_data[0]['tour_idx'] = tour_idx
        current_tour_data[0]['vehicle_id'] = vehicle_id
        
        # Create map
        map_obj = _create_editable_tour_map(tour_df, df_geocoded, vehicle_id)
        
        # Display map
        with map_output:
            display(HTML(map_obj._repr_html_()))
        
        # Create stops list with reorder controls
        _create_stops_list_ui(tour_df, stops_output, control_output, 
                             updated_vrp_response, vehicle_id, map_output, df_geocoded, current_tour_data)
    
    def on_tour_change(change):
        """Handle tour selection change"""
        if change['type'] == 'change' and change['name'] == 'value':
            update_tour_display(change['new'])
    
    tour_selector.observe(on_tour_change, names='value')
    
    # Initial display
    if tours:
        update_tour_display(0)
    
    # Layout
    header = widgets.HTML(
        value="<h3>🎯 Interactive Tour Editor</h3><p>Select a tour and reorder stops using the controls below.</p>",
        layout=widgets.Layout(margin='10px 0px')
    )
    
    ui = widgets.VBox([
        header,
        tour_selector,
        widgets.HBox([
            widgets.VBox([widgets.HTML("<b>Tour Map</b>"), map_output], layout=widgets.Layout(width='60%')),
            widgets.VBox([widgets.HTML("<b>Stops List (Reorder Here)</b>"), stops_output], layout=widgets.Layout(width='40%'))
        ]),
        control_output
    ])
    
    display(ui)
    
    return updated_vrp_response


def _create_merged_df_from_vrp(vrp_response_json: dict, df_geocoded: pd.DataFrame) -> pd.DataFrame:
    """Create merged_df from VRP response (similar to module_results)"""
    all_activities = []
    
    for tour in vrp_response_json.get('tours', []):
        vehicle_id = tour.get('vehicleId')
        type_id = tour.get('typeId')
        
        for stop in tour.get('stops', []):
            for activity in stop.get('activities', []):
                all_activities.append({
                    "Vehicle ID": vehicle_id,
                    "Type ID": type_id,
                    "Job ID": activity.get("jobId"),
                    "Activity Type": activity.get("type"),
                    "Latitude": activity.get("location", {}).get("lat", 0),
                    "Longitude": activity.get("location", {}).get("lng", 0),
                    "Start Time": activity.get("time", {}).get("start", ""),
                    "End Time": activity.get("time", {}).get("end", ""),
                    "Distance": stop.get("distance", 0)
                })
    
    activities_df = pd.DataFrame(all_activities)
    merged_df = pd.merge(activities_df, df_geocoded, 
                        left_on='Job ID', right_on='Auftr.-Nr.', how='left')
    
    return merged_df


def _create_editable_tour_map(tour_df: pd.DataFrame, df_geocoded: pd.DataFrame, 
                              vehicle_id: str) -> folium.Map:
    """Create a Folium map showing the tour route"""
    if tour_df.empty:
        center_lat, center_lng = 52.5, 13.4  # Default (Berlin)
    else:
        center_lat = tour_df['Latitude'].mean()
        center_lng = tour_df['Longitude'].mean()
    
    m = folium.Map(location=[center_lat, center_lng], zoom_start=11)
    
    # Get tour points in order
    tour_points = tour_df[['Latitude', 'Longitude']].values.tolist()
    
    # Draw route
    folium.PolyLine(
        tour_points, 
        color='blue', 
        weight=4, 
        opacity=0.7,
        tooltip=f'Tour: {vehicle_id}'
    ).add_to(m)
    
    # Add markers for each stop
    for idx, row in tour_df.iterrows():
        job_id = row.get('Job ID', 'N/A')
        activity_type = row.get('Activity Type', 'N/A')
        start_time = row.get('Start Time', 'N/A')
        
        # Get customer info
        customer_name = 'N/A'
        address = 'N/A'
        order_info = df_geocoded[df_geocoded['Auftr.-Nr.'] == job_id]
        if not order_info.empty:
            order_row = order_info.iloc[0]
            if activity_type == 'delivery':
                customer_name = order_row.get('Empfänger', 'N/A')
                address = order_row.get('dropoff_label', 'N/A')
            elif activity_type == 'pickup':
                customer_name = order_row.get('Vers.-Name', 'N/A')
                address = order_row.get('pickup_label', 'N/A')
        
        # Create popup
        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 5px 0;">Stop {idx + 1}</h4>
            <p><b>Job ID:</b> {job_id}<br>
            <b>Type:</b> {activity_type}<br>
            <b>Customer:</b> {customer_name}<br>
            <b>Address:</b> {address}<br>
            <b>Time:</b> {start_time}</p>
        </div>
        """
        
        # Choose icon based on activity type
        if idx == 0:
            icon = folium.Icon(color='green', icon='home', prefix='fa')
        elif activity_type == 'pickup':
            icon = folium.Icon(color='blue', icon='arrow-up', prefix='fa')
        else:
            icon = folium.Icon(color='red', icon='arrow-down', prefix='fa')
        
        # Add marker
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=icon,
            tooltip=f"Stop {idx + 1}: {job_id} ({activity_type})"
        ).add_to(m)
        
        # Add stop number label
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=15,
            popup=f"Stop {idx + 1}",
            color='white',
            fill=True,
            fillColor='blue',
            fillOpacity=0.8,
            weight=2
        ).add_to(m)
        
        # Add number text
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; font-weight: bold; color: white; text-align: center; line-height: 30px;">{idx + 1}</div>',
                icon_size=(30, 30),
                icon_anchor=(15, 15)
            )
        ).add_to(m)
    
    return m


def _create_stops_list_ui(tour_df: pd.DataFrame, stops_output: widgets.Output,
                          control_output: widgets.Output, vrp_response_json: dict,
                          vehicle_id: str, map_output: widgets.Output,
                          df_geocoded: pd.DataFrame, current_tour_data: list):
    """Create interactive stops list with reorder buttons"""
    
    stops_list = []
    stop_widgets = []
    
    for idx, row in tour_df.iterrows():
        job_id = row.get('Job ID', 'N/A')
        activity_type = row.get('Activity Type', 'N/A')
        start_time = row.get('Start Time', 'N/A')
        
        # Get customer info
        customer_name = 'N/A'
        order_info = df_geocoded[df_geocoded['Auftr.-Nr.'] == job_id]
        if not order_info.empty:
            order_row = order_info.iloc[0]
            if activity_type == 'delivery':
                customer_name = order_row.get('Empfänger', 'N/A')
            elif activity_type == 'pickup':
                customer_name = order_row.get('Vers.-Name', 'N/A')
        
        # Create stop widget
        stop_num = widgets.HTML(
            value=f"<b style='font-size: 18px; color: blue;'>{idx + 1}</b>",
            layout=widgets.Layout(width='40px')
        )
        
        stop_info = widgets.HTML(
            value=f"""
            <div style='padding: 5px;'>
                <b>{activity_type.upper()}</b> - Job {job_id}<br>
                <small>{customer_name[:30]}</small><br>
                <small style='color: gray;'>{start_time}</small>
            </div>
            """,
            layout=widgets.Layout(width='300px', margin='5px')
        )
        
        # Move buttons
        move_up_btn = widgets.Button(
            description='↑',
            button_style='info',
            tooltip='Move up',
            layout=widgets.Layout(width='40px', height='40px')
        )
        
        move_down_btn = widgets.Button(
            description='↓',
            button_style='info',
            tooltip='Move down',
            layout=widgets.Layout(width='40px', height='40px')
        )
        
        # Store row index for reordering
        move_up_btn.row_idx = idx
        move_down_btn.row_idx = idx
        
        # Button handlers
        def create_move_handler(direction, row_idx, current_df):
            def handler(b):
                _move_stop(current_df, row_idx, direction, stops_output, control_output,
                          vrp_response_json, vehicle_id, map_output, df_geocoded, current_tour_data)
            return handler
        
        move_up_btn.on_click(create_move_handler('up', idx, tour_df))
        move_down_btn.on_click(create_move_handler('down', idx, tour_df))
        
        # Disable buttons at edges
        if idx == 0:
            move_up_btn.disabled = True
        if idx == len(tour_df) - 1:
            move_down_btn.disabled = True
        
        # Create row
        row_widget = widgets.HBox([
            stop_num,
            stop_info,
            widgets.VBox([move_up_btn, move_down_btn], layout=widgets.Layout(width='50px'))
        ], layout=widgets.Layout(
            border='1px solid #ccc',
            padding='5px',
            margin='2px',
            width='100%'
        ))
        
        stop_widgets.append(row_widget)
        stops_list.append({
            'row': row,
            'widget': row_widget,
            'index': idx
        })
    
    # Apply button
    apply_btn = widgets.Button(
        description='✅ Apply Changes',
        button_style='success',
        layout=widgets.Layout(width='200px', height='40px', margin='10px')
    )
    
    def apply_changes_handler(b):
        current_df = current_tour_data[0]['tour_df']
        _apply_reorder_to_vrp(current_df, vrp_response_json, vehicle_id, control_output)
    
    apply_btn.on_click(apply_changes_handler)
    
    # Display
    with stops_output:
        display(widgets.VBox(stop_widgets + [apply_btn]))
    
    with control_output:
        print("💡 Tip: Use ↑ and ↓ buttons to reorder stops, then click 'Apply Changes' to save.")


def _move_stop(tour_df: pd.DataFrame, row_idx: int, direction: str,
               stops_output: widgets.Output, control_output: widgets.Output,
               vrp_response_json: dict, vehicle_id: str,
               map_output: widgets.Output, df_geocoded: pd.DataFrame,
               current_tour_data: list):
    """Move a stop up or down in the order"""
    new_idx = row_idx - 1 if direction == 'up' else row_idx + 1
    
    if new_idx < 0 or new_idx >= len(tour_df):
        return
    
    # Swap rows - need to work with the stored dataframe
    current_df = current_tour_data[0]['tour_df'].copy()
    current_df.iloc[row_idx], current_df.iloc[new_idx] = current_df.iloc[new_idx].copy(), current_df.iloc[row_idx].copy()
    
    # Reset index
    current_df = current_df.reset_index(drop=True)
    
    # Update stored dataframe
    current_tour_data[0]['tour_df'] = current_df
    
    # Update display
    with control_output:
        clear_output()
        print(f"✅ Moved stop {row_idx + 1} {'up' if direction == 'up' else 'down'}. Click 'Apply Changes' to save.")
    
    # Refresh UI
    _create_stops_list_ui(current_df, stops_output, control_output,
                         vrp_response_json, vehicle_id, map_output, df_geocoded, current_tour_data)
    
    # Update map
    map_obj = _create_editable_tour_map(current_df, df_geocoded, vehicle_id)
    with map_output:
        clear_output(wait=True)
        display(HTML(map_obj._repr_html_()))


def _apply_reorder_to_vrp(tour_df: pd.DataFrame, vrp_response_json: dict,
                          vehicle_id: str, control_output: widgets.Output):
    """Apply the reordered stops to the VRP response"""
    # Find the tour
    for tour in vrp_response_json.get('tours', []):
        if tour.get('vehicleId') == vehicle_id:
            # Create a mapping of job+activity to original stop data
            activity_map = {}
            for stop in tour.get('stops', []):
                for activity in stop.get('activities', []):
                    key = (str(activity.get('jobId')), activity.get('type'))
                    activity_map[key] = {
                        'activity': activity,
                        'distance': stop.get('distance', 0)
                    }
            
            # Rebuild stops based on new order from tour_df
            new_stops = []
            
            for idx, row in tour_df.iterrows():
                job_id = str(row['Job ID'])
                activity_type = row['Activity Type']
                key = (job_id, activity_type)
                
                if key in activity_map:
                    # Create new stop with this activity
                    new_stop = {
                        'activities': [activity_map[key]['activity']],
                        'distance': activity_map[key]['distance']
                    }
                    new_stops.append(new_stop)
            
            # Update tour
            tour['stops'] = new_stops
            
            with control_output:
                clear_output()
                print("✅ Changes applied! Tour order has been updated.")
                print("   You can now continue with your workflow using the updated vrp_response_json.")
            
            break


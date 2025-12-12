import math
import folium
from datetime import datetime
from folium.features import DivIcon


def create_map(tours_assigned_df, df_geocoded, unassigned_jobs_data, base_date_str):
    # Initializing the map
    map_center_lat = tours_assigned_df['Latitude'].mean()
    map_center_lng = tours_assigned_df['Longitude'].mean()
    m = folium.Map(location=[map_center_lat, map_center_lng], zoom_start=9)

    colors = [
        'red',
        'blue',
        'gray',
        'darkred',
        'orange',
        'green',
        'darkgreen',
        'lightgreen',
        'darkblue',
        'lightblue',
        'purple',
        'darkpurple',
        'pink',
        'cadetblue',
        'black'
    ]

    # Function to apply a small offset to latitude and longitude
    def apply_offset(latitude, longitude, idx, total_count):
        # Calculate offset
        offset_angle = 360 / total_count * idx
        offset_distance = 0.005  # Small distance offset
        rad = offset_angle * (3.141592 / 180.0)

        new_latitude = latitude + (offset_distance * math.cos(rad))
        new_longitude = longitude + (offset_distance * math.sin(rad))
        return new_latitude, new_longitude
    
    # Function to create markers for each unassigned job/order
    def create_unassigned_markers(df, tours_assigned_df):
        reduced_df = df[~df["Auftr.-Nr."].isin(tours_assigned_df["Job ID"])]

        for idx, row in reduced_df.iterrows():
            popup_content = f"<b>Date:</b> {row['Entl. bis (Auftr.)'].strftime('%Y-%m-%d %H:%M:%S')}<br>"
            for col in ['customer_branch_cluster', 'Entladeart', 'pickup_label',  'dropoff_label', 'customer_shipment_weight_kg', 'customer_shipment_volume_units', 'day', 'Auftr.-Nr.' ]:
                if col == 'customer_shipment_volume_units':
                    popup_content += f"<b>{col}:</b> {row[col]/10}<br>"
                else:
                    popup_content += f"<b>{col}:</b> {row[col]}<br>"
            popup = folium.Popup(popup_content, max_width=300)

            folium.Marker(
                location=[row['dropoff_lat'], row['dropoff_lng']],
                popup=popup
            ).add_to(m)

    # Add markers for not assigned orders
    create_unassigned_markers(df_geocoded, tours_assigned_df)

    # Create a tour per vehicle
    for index, ((vehicle_id), group) in enumerate(tours_assigned_df.groupby(['Vehicle ID'])):
        tour_points = group[['Latitude', 'Longitude']].values.tolist()
        tour_color = colors[index % len(colors)]
        vehicle_name = group['Vehicle ID'].iloc[0] if 'Vehicle ID' in group.columns else f'Vehicle {vehicle_id}'

        folium.PolyLine(tour_points, color=tour_color, weight=3, opacity=0.8, tooltip=f'{vehicle_name}').add_to(m)

        # Initialize stop index counter for each vehicle
        stop_index = 1

        # Create stops per vehicle with a popup
        for idx, row in group.iterrows():
            popup_content = ""  # Initialize popup_content for each stop
            start_time = row['Start Time']
            #space = row['customer_shipment_volume_units']/10
            weight = row['customer_shipment_weight_kg']
            job_id = row['Job ID']
            activity_type = row['Activity Type']
            popup_content += f"<b>Vehicle ID:</b> {row['Vehicle ID']}<br>"
            popup_content += f"<b>Vehicle:</b> {vehicle_name}<br>"
            for col in ['Job ID', 'customer_shipment_weight_kg', 'customer_shipment_volume_units','Activity Type', 'Latitude', 'Longitude', 'End Time', 'Distance']:  # Specify columns to include
                popup_content += f"<b>{col}:</b> {row[col]}<br>"
            popup = folium.Popup(popup_content, max_width=300)

            # differentiate first and all other stops, to display first as home depot
            if idx == group.index[0]:
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=popup,
                    icon=folium.Icon(color=tour_color, icon='home'),
                ).add_to(m)
            else:
                # Apply offset to latitude and longitude for visibility
                offset_lat, offset_lng = apply_offset(row['Latitude'], row['Longitude'], idx, len(group))
                folium.Marker(
                    location=[offset_lat, offset_lng],
                    icon=DivIcon(
                        icon_size=(100,10),
                        icon_anchor=(0,0),
                        #html=f'<div style="font-size: 7pt; font-weight: bold; color: white; background-color: {tour_color}; padding: 1px; border-radius: 1px;">({stop_index}) Job: {job_id} ({activity_type}: {start_time} Space: {space} Weight: {weight}</div>'
                        #html=f'<div style="font-size: 7pt; font-weight: bold; color: white; background-color: {tour_color}; padding: 1px; border-radius: 1px;">({stop_index}) {job_id} ({activity_type}: {start_time}) {space} PAL & {weight} kg</div>'
                        )
                    ).add_to(m),
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=5,
                    color=tour_color,
                    fill_color=tour_color,
                    popup=popup
                ).add_to(m)

                # Increment the stop index for the next stop
                stop_index += 1

    # Adding a legend
    legend_html = '<div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; font-size:14px; background:white; padding:10px;">'
    legend_html += '<b> Vehicle Legend </b><br>'
    for i, (vehicle_id, group) in enumerate(tours_assigned_df.groupby(['Vehicle ID'])):
        vehicle_name = group['Vehicle Name'].iloc[0] if 'Vehicle Name' in group.columns else f'Vehicle {vehicle_id}'
        color = colors[i % len(colors)]
        legend_html += f'<i style="background:{color};width:12px;height:12px;display:inline-block;margin-right:5px;"></i> {vehicle_name}<br>'
    legend_html += '<br>'"Unassigned orders: " + str(len(unassigned_jobs_data)) + '<br>'
    legend_html += "Day: " + base_date_str

    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    return m
   


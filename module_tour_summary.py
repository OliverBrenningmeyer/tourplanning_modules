"""
Tour summary module for displaying tour planning statistics.
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List


def generate_tour_summary(vrp_response_json: dict, merged_df: pd.DataFrame, unassigned_jobs: List[dict]) -> pd.DataFrame:
    """
    Generate a summary of tours with statistics.
    
    Args:
        vrp_response_json: The VRP response JSON from HERE API
        merged_df: Merged DataFrame with tour activities
        unassigned_jobs: List of unassigned jobs
        
    Returns:
        DataFrame with tour summary statistics
    """
    tour_summaries = []
    
    # Process each tour from VRP response
    for tour in vrp_response_json.get('tours', []):
        vehicle_id = tour.get('vehicleId', 'Unknown')
        type_id = tour.get('typeId', 'Unknown')
        
        # Get tour statistics from VRP response
        statistics = tour.get('statistics', {})
        duration = statistics.get('duration', 0)  # in seconds
        distance = statistics.get('distance', 0)  # in meters
        
        # Get start and end times from first and last stops
        stops = tour.get('stops', [])
        start_time = None
        end_time = None
        
        if stops:
            first_stop = stops[0]
            last_stop = stops[-1]
            
            # Get start time from first activity of first stop
            if first_stop.get('activities'):
                first_activity = first_stop['activities'][0]
                start_time = first_activity.get('time', {}).get('start', 'N/A')
            
            # Get end time from last activity of last stop
            if last_stop.get('activities'):
                last_activity = last_stop['activities'][-1]
                end_time = last_activity.get('time', {}).get('end', 'N/A')
        
        # Count stops (excluding depot start/end if they're just location markers)
        # Count unique job IDs from merged_df for this vehicle
        vehicle_activities = merged_df[merged_df['Vehicle ID'] == vehicle_id]
        unique_jobs = vehicle_activities['Job ID'].nunique()
        total_stops = len(vehicle_activities[vehicle_activities['Activity Type'].isin(['pickup', 'delivery'])])
        
        # Count pickups and deliveries
        pickups = len(vehicle_activities[vehicle_activities['Activity Type'] == 'pickup'])
        deliveries = len(vehicle_activities[vehicle_activities['Activity Type'] == 'delivery'])
        
        # If statistics not available, calculate from merged_df
        if duration == 0 and not vehicle_activities.empty:
            # Calculate duration from start and end times if available
            if 'Start Time' in vehicle_activities.columns and 'End Time' in vehicle_activities.columns:
                try:
                    # Get first start time and last end time
                    start_times = pd.to_datetime(vehicle_activities['Start Time'], errors='coerce')
                    end_times = pd.to_datetime(vehicle_activities['End Time'], errors='coerce')
                    if not start_times.isna().all() and not end_times.isna().all():
                        first_start = start_times.min()
                        last_end = end_times.max()
                        if pd.notna(first_start) and pd.notna(last_end):
                            duration = (last_end - first_start).total_seconds()
                except:
                    pass
        
        # If distance not available, sum from merged_df
        # Note: Distance from VRP API is typically in meters, but check the actual values
        if distance == 0 and not vehicle_activities.empty and 'Distance' in vehicle_activities.columns:
            try:
                distance_sum = vehicle_activities['Distance'].sum()
                # If values seem small (< 1000), they might be in km, otherwise assume meters
                if distance_sum > 0 and distance_sum < 100:
                    distance = distance_sum * 1000  # Convert km to meters
                else:
                    distance = distance_sum  # Already in meters
            except:
                pass
        
        tour_summaries.append({
            'Vehicle ID': vehicle_id,
            'Type ID': type_id,
            'Stops': total_stops,
            'Jobs': unique_jobs,
            'Pickups': pickups,
            'Deliveries': deliveries,
            'Duration (hours)': round(duration / 3600, 2),
            'Distance (km)': round(distance / 1000, 2),
            'Start Time': start_time,
            'End Time': end_time
        })
    
    # Create DataFrame
    summary_df = pd.DataFrame(tour_summaries)
    
    # Add totals row
    if not summary_df.empty:
        totals = {
            'Vehicle ID': 'TOTAL',
            'Type ID': '-',
            'Stops': summary_df['Stops'].sum(),
            'Jobs': summary_df['Jobs'].sum(),
            'Pickups': summary_df['Pickups'].sum(),
            'Deliveries': summary_df['Deliveries'].sum(),
            'Duration (hours)': round(summary_df['Duration (hours)'].sum(), 2),
            'Distance (km)': round(summary_df['Distance (km)'].sum(), 2),
            'Start Time': '-',
            'End Time': '-'
        }
        summary_df = pd.concat([summary_df, pd.DataFrame([totals])], ignore_index=True)
    
    return summary_df


def display_tour_summary(vrp_response_json: dict, merged_df: pd.DataFrame, unassigned_jobs: List[dict], 
                        base_date_str: str, display_in_colab: bool = True):
    """
    Display tour summary in a formatted way.
    
    Args:
        vrp_response_json: The VRP response JSON
        merged_df: Merged DataFrame with tour activities
        unassigned_jobs: List of unassigned jobs
        base_date_str: Planning date string
        display_in_colab: Whether to use Colab display formatting
    """
    summary_df = generate_tour_summary(vrp_response_json, merged_df, unassigned_jobs)
    
    print("=" * 80)
    print("TOUR PLANNING SUMMARY")
    print("=" * 80)
    print(f"Planning Date: {base_date_str}")
    print()
    
    if summary_df.empty:
        print("⚠️  No tours generated")
        return
    
    # Display summary table
    print("Tour Statistics:")
    print("-" * 80)
    
    # Format the display
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 20)
    
    print(summary_df.to_string(index=False))
    print()
    
    # Display unassigned jobs
    print("-" * 80)
    print(f"Unassigned Jobs: {len(unassigned_jobs)}")
    if unassigned_jobs:
        print("Unassigned Job IDs:")
        for job in unassigned_jobs[:10]:  # Show first 10
            print(f"  - {job.get('Job ID', 'Unknown')}: {job.get('Reasons', 'No reason provided')}")
        if len(unassigned_jobs) > 10:
            print(f"  ... and {len(unassigned_jobs) - 10} more")
    print("=" * 80)
    
    return summary_df


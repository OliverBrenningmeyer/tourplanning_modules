import pandas as pd
import requests
import numpy as np
import json
from datetime import datetime
from module_client_configuration import CONFIG

def vrp_problem_definition(df: pd.DataFrame, api_key: str, depots_path: str, base_date_str: str, product_category: str, client_name: str) -> dict:
    """
    Generate a JSON structured object for vehicle routing planning.
    """
    
    # Function to load DataFrame from Excel file
    def load_dataframe(file_path):
        return pd.read_excel(file_path, engine='openpyxl')

    # Function to filter depots
    def filter_depots(depots_all):
        return depots_all[depots_all['active_Dispobereich'].notna()]

    # Update the generate_shifts function to use the configuration values
    def generate_shifts(lat, lng, base_date, shift_type, start_time, end_time,client_name):
        base_date_str = datetime.strptime(base_date, "%Y-%m-%d").date()
        shifts = []
        config = CONFIG.get(client_name, CONFIG["default"])

        shifts.append({
            "start": {"time": f"{base_date_str}T{start_time}Z", "location": {"lat": lat, "lng": lng}}, # definiton of start time and location
            #"start": {"time": f"{base_date_str}T{start_time}Z"}, # definiton of start time without location
            "end": {"time": f"{base_date_str}T{end_time}Z"}, # definition of end time without location
            #"end": {"time": f"{base_date_str}T{end_time}Z", "location": {"lat": lat, "lng": lng}}, # definition of end time and location
            "breaks": [{
                "duration": config["break_duration"][shift_type],
                "times": [[f"{base_date_str}T{config['break_times'][shift_type][0]}Z", f"{base_date_str}T{config['break_times'][shift_type][1]}Z"]]
            }]
        })
        return shifts

    # Updated generate_fleet_types to handle both dedicated and open vehicles
    def generate_fleet_types(depots, base_date_str,client_name):
        fleet_types = []
        fleet_config = CONFIG[client_name]["fleet"]

        # Dedicated vehicles based on depots
        for _, row in depots.iterrows():
            for shift_type in ['fullDay', 'halfDay']:
                if not pd.isna(row[f"count_{shift_type}"]):
                    shifts = generate_shifts(row['here_lat'], row['here_lng'], base_date_str, shift_type,
                                             row[f"startTime_{shift_type}"], row[f"endTime_{shift_type}"],client_name)

                    # Get strict value from config, ensure boolean True/False
                    strict_value = (
                        CONFIG.get(client_name, {})
                        .get("dedicated_branches", {})
                        .get("customer_branch_cluster", {})
                        .get(str(row['Dispobereich']), {})
                        .get("strict_territory", False)
                    )
                    strict_bool = bool(strict_value) if isinstance(strict_value, bool) else str(strict_value).lower() == "true"

                    fleet_types.append({
                        "id": f"{prefix_depot_vehicles}{row['Dispobereich']}-{int(row[f'price_{shift_type}'])}-{row[f'salesVehicleClass_{shift_type}']}-{int(row[f'buyingprice_{shift_type}'])}",
                        "profile": f"vehicle_{shift_type}",
                        "speedFactor": fleet_config["dedicatedVehicles"]["speedFactor"],
                        "costs": {
                            "fixed": int(row[f"price_{shift_type}"]),
                            "distance": fleet_config["dedicatedVehicles"]["costs"]["distance"][shift_type],
                            "time": fleet_config["dedicatedVehicles"]["costs"]["time"][shift_type]
                        },
                        "territories": {
                            "strict": strict_bool,
                            "items": [{"id": row['Dispobereich']}]
                        },
                        "shifts": shifts,
                        "capacity": [int(row[f'capacity_{shift_type}']), int(row[f'capacity_weight_{shift_type}'])],
                        "limits": {
                            "maxDistance": fleet_config["dedicatedVehicles"]["limits"]["maxDistance"][shift_type],
                            "shiftTime": fleet_config["dedicatedVehicles"]["limits"]["shiftTime"][shift_type]
                        },
                        "skills": ([row[f"salesVehicleClass_{shift_type}"]] if isinstance(row[f"salesVehicleClass_{shift_type}"], str) else row[f"salesVehicleClass_{shift_type}"]) + ["DEFAULT_SKILL"],
                        "amount": int(row[f"count_{shift_type}"])
                    })

        # Open vehicles from configuration fleet IDs
        for fleet_id, open_vehicle_config in fleet_config["openVehicles"]["fleet_ids"].items():
            fleet_types.append({
                "id": f"{prefix_openVehicles}{fleet_id}",
                "profile": "vehicle_openVehicle",
                "speedFactor": open_vehicle_config["speedFactor"],
                "costs": {
                    "fixed": open_vehicle_config["costs"]["fixed"],
                    "distance": open_vehicle_config["costs"]["distance"],
                    "time": open_vehicle_config["costs"]["time"]
                },
                "shifts": [
                    {
                        "start": {"time": f"{base_date_str}T{open_vehicle_config['shifts'][0]['start']}Z"},
                        "end": {"time": f"{base_date_str}T{open_vehicle_config['shifts'][0]['end']}Z"}
                    }
                ],
                "capacity": [int(cap) for cap in open_vehicle_config["capacity"]],
                "skills": open_vehicle_config["skills"] if isinstance(open_vehicle_config["skills"], list) else [open_vehicle_config["skills"]],
                "amount": int(open_vehicle_config["amount"])
            })

        return fleet_types

    def generate_jobs(df, base_date_str, client_name):
        jobs = []
        job_config = CONFIG[client_name]["job"]
        timewindow_config = CONFIG[client_name]["order"].get("timewindow", True)  # set to true if no value is provided

        for _, row in df.iterrows():
            # Use pickup geocoordinates from CONFIG per customer_branch_cluster if available
            pickup_geocodes = CONFIG.get(client_name, {}).get("dedicated_branches", {}).get("customer_branch_cluster", {})
            cluster = row['customer_branch_cluster']
            if cluster in pickup_geocodes:
                # Get strict value for this cluster from config
                # Check if earlier_pickup_times are defined for this cluster in CONFIG
                earliest_pickup_time = pickup_geocodes[cluster].get("earliest_pickup_time")
                latest_pickup_time = pickup_geocodes[cluster].get("latest_pickup_time")


                pickup_place = {
                    "location": {
                        "lat": float(pickup_geocodes[cluster]["pickup_lat"]),
                        "lng": float(pickup_geocodes[cluster]["pickup_lng"])
                    },
                    "duration": job_config["pickup_duration"],
                    "territoryIds": [cluster]
                }
                # Add times if earlier_pickup_times is defined
                if earliest_pickup_time and latest_pickup_time:
                    pickup_place["times"] = [[
                        f"{base_date_str}T{earliest_pickup_time}Z",
                        f"{base_date_str}T{latest_pickup_time}Z"
                    ]]

                job = {
                    "id": str(row["Auftr.-Nr."]),
                    "tasks": {
                        "pickups": [{
                            "places": [pickup_place],
                            "demand": [
                                max(int(row['customer_shipment_volume_units']), 0.1),
                                max(int(row['customer_shipment_weight_kg']), 1)
                            ]
                        }],
                        "deliveries": [{
                            "places": [{
                                "times": [[row['Termin von ISO'], row['Termin bis ISO']]] if timewindow_config else [[base_date_str + 'T07:00:00Z', base_date_str + 'T17:00:00Z']],
                                "location": {
                                    "lat": float(row['dropoff_lat']),
                                    "lng": float(row['dropoff_lng'])
                                },
                                "duration": job_config["delivery_duration"],
                                "territoryIds": [cluster]
                            }],
                            "demand": [
                                max(int(row['customer_shipment_volume_units']), 0.1),
                                max(int(row['customer_shipment_weight_kg']), 1)
                            ]
                        }]
                    }
                }
            else:
                job = {
                    "id": str(row["Auftr.-Nr."]),
                    "tasks": {
                        "pickups": [{
                            "places": [{
                                "location": {"lat": row['pickup_lat'], "lng": row['pickup_lng']},
                                "duration": job_config["pickup_duration"],
                                "territoryIds": [row['customer_branch_cluster']]
                            }],
                            "demand": [max(int(row['customer_shipment_volume_units']), 0.1), max(int(row['customer_shipment_weight_kg']), 1)]
                        }],
                        "deliveries": [{
                            "places": [{
                                "times": [[row['Termin von ISO'], row['Termin bis ISO']]] if timewindow_config else [[base_date_str + 'T07:00:00Z', base_date_str + 'T17:00:00Z']],
                                "location": {"lat": row['dropoff_lat'], "lng": row['dropoff_lng']},
                                "duration": job_config["delivery_duration"],
                                "territoryIds": [row['customer_branch_cluster']]
                            }],
                            "demand": [max(int(row['customer_shipment_volume_units']), 0.1), max(int(row['customer_shipment_weight_kg']), 1)]
                        }]
                    }
                }

            # Assign skills based on 'Entladeart' column
            # Handle missing values explicitly.
            if pd.isna(row['Entladeart']):
                job["skills"] = ["DEFAULT_SKILL"]  # Assign a default skill for missing 'Entladeart'
            elif row['Entladeart'] in ["Hebebühne", "Entladung ebenerdig"]:
                job["skills"] = ["SPRINTER_TAIL_LIFT"]
            elif not pd.isna(row['Entladeart']):
                job["skills"] = ["SPRINTER_TAIL_LIFT"]

            jobs.append(job)
        return jobs

    # Define prefix for vehicle ID based on the product category to ensure proper mapping in bexOS
    prefix_depot_vehicles = "openVehicle-" if product_category == "bex Kurier" else ("dedicatedVehicle-" if product_category == "bex Tour" else "")
    prefix_openVehicles = "dedicatedVehicle-" if product_category == "bex Tour" else ("openVehicle-")

    # Load depots DataFrame
    depots_all = load_dataframe(depots_path)
    print(f"Depots DataFrame loaded with {len(depots_all)} rows.")

    # Filter depots
    depots = filter_depots(depots_all)
    print(f"Filtered depots DataFrame with {len(depots)} rows.")

    # Generate fleet types
    fleet_types = generate_fleet_types(depots, base_date_str,client_name)
    print(f"Generated {len(fleet_types)} fleet types.")

    # Generate jobs
    jobs = generate_jobs(df, base_date_str,client_name)
    print(f"Generated {len(jobs)} jobs.")

    # Construct the final JSON
    dynamic_json = {
        "fleet": {
            "types": fleet_types,
            "profiles": [{"type": "car", "name": f"vehicle_{shift_type}"} for shift_type in ['fullDay', 'halfDay','openVehicle']],
            "traffic": "historicalOnly"
        },
        "plan": {
            "jobs": jobs
        },
        "configuration": {
            "experimentalFeatures": ["advancedObjectives"] #https://www.here.com/docs/bundle/tour-planning-api-api-reference/page/index.html#tag/Synchronous/paths/~1problems/post
        },
        "advancedObjectives": CONFIG[client_name]["advancedObjectives"]
    }
    print("Dynamic JSON object created.")

    return dynamic_json

def vrp_problem_execution(request_body,api_key:str):
    """
    Execute the generated problem statement for the actual external vehicle routing planning.
    """
    # The URL for the VRP API endpoint
    vrp_url = 'https://tourplanning.hereapi.com/v3/problems'

    # Add the API key to the query parameters instead of the body or headers
    response = requests.post(vrp_url, params={'apikey': api_key}, headers={'Content-Type': 'application/json'}, json=request_body)

    # Properly handle API request failures by initializing 'response_data'
    response_data = {"error": "API request failed", "status_code": response.status_code, "details": response.text}  # Initialize with error details
    if response.status_code == 200:
        print("Request for VRP_Execution to HERE was successful.")
        response_data = response.json()
    else:
        print(f"VRP Request to HERE failed with status code: {response.status_code}")
        print(response.text)
    
    return response_data
import time

import numpy as np
import pandas as pd
import requests

from module_client_configuration import CONFIG

def geocoding_cleaned_data(df: pd.DataFrame,api_key: str,client_name: str) -> pd.DataFrame:
    """
    Geocode addresses in the DataFrame using HERE API.
    The function takes a DataFrame with address columns and returns a new DataFrame
    with additional columns containing latitude, longitude, and other geocoding information.
    The function assumes the DataFrame has the following columns:
    - 'Vers.-Str.': Street address for pickup
    - 'Vers.-PLZ': Postal code for pickup
    - 'Vers.-Ort': City for pickup
    - 'Empf.-Str.': Street address for dropoff
    - 'Empf.-PLZ': Postal code for dropoff
    - 'Empf.-Ort': City for dropoff
    The function uses the HERE API for geocoding and requires an API key.
    The function handles errors gracefully and assigns NaN or None to missing values in the response.
    The function also handles cases where the API request fails or the response is not in the expected format.
    The function returns a DataFrame with the following additional columns:
    - 'pickup_lat': Latitude for pickup
    - 'pickup_lng': Longitude for pickup
    - 'pickup_id': ID from HERE response for pickup
    - 'pickup_input': Input address from HERE response for pickup
    - 'pickup_label': Label from HERE response for pickup
    - 'pickup_countryCode': Country code from HERE response for pickup
    - 'pickup_city': City from HERE response for pickup
    - 'pickup_street': Street from HERE response for pickup
    - 'pickup_postalCode': Postal code from HERE response for pickup
    - 'pickup_houseNumber': House number from HERE response for pickup
    - 'pickup_queryScore': Query score from HERE response for pickup
    - 'dropoff_lat': Latitude for dropoff
    - 'dropoff_lng': Longitude for dropoff
    - 'dropoff_id': ID from HERE response for dropoff
    - 'dropoff_input': Input address from HERE response for dropoff
    - 'dropoff_label': Label from HERE response for dropoff
    - 'dropoff_countryCode': Country code from HERE response for dropoff
    - 'dropoff_city': City from HERE response for dropoff
    - 'dropoff_street': Street from HERE response for dropoff
    - 'dropoff_postalCode': Postal code from HERE response for dropoff
    - 'dropoff_houseNumber': House number from HERE response for dropoff
    - 'dropoff_queryScore': Query score from HERE response for dropoff

    Returns DataFrame with geocording results in additional columns .
    """

    # Function to call the API and get latitude and longitude and other values from HERE response
    def get_lat_lng_and_more(address, api_key):
        url = "https://geocode.search.hereapi.com/v1/geocode"
        params = {'q': address, 'apiKey': api_key}
        max_attempts = 5
        backoff_seconds = 1

        for attempt in range(max_attempts):
            try:
                response = requests.get(url, params=params)

                if response.status_code == 429:
                    retry_after_header = response.headers.get("Retry-After")
                    retry_after = float(retry_after_header) if retry_after_header else backoff_seconds
                    retry_after = max(retry_after, 1)
                    print(f"HERE API rate limit reached for '{address}'. Waiting {retry_after:.1f}s before retrying "
                          f"(attempt {attempt + 1} of {max_attempts}).")
                    time.sleep(retry_after)
                    backoff_seconds *= 2
                    continue

                response.raise_for_status()  # Raise an HTTPError for bad status codes
                response_json = response.json()

                # Extract information from the response JSON with error handling for missing keys
                location = response_json['items'][0]['position']
                lat = location.get('lat', np.nan)  # Assign NaN if 'lat' key is missing
                lng = location.get('lng', np.nan)  # Assign NaN if 'lng' key is missing

                address_info = response_json['items'][0]['address']
                id_ = response_json['items'][0].get('id', None)  # Assign None if 'id' key is missing
                input_ = response_json['items'][0].get('title', None)  # Assign None if 'title' key is missing
                label = address_info.get('label', None)  # Assign None if 'label' key is missing
                countryCode = address_info.get('countryCode', None)  # Assign None if 'countryCode' key is missing
                city = address_info.get('city', None)  # Assign None if 'city' key is missing
                street = address_info.get('street', None)  # Assign None if 'street' key is missing
                postalCode = address_info.get('postalCode', None)  # Assign None if 'postalCode' key is missing
                houseNumber = address_info.get('houseNumber', None)  # Assign None if 'houseNumber' key is missing

                queryScore = response_json['items'][0]['scoring'].get('queryScore', None)  # Assign None if 'queryScore' key is missing

                return lat, lng, id_, input_, label, countryCode, city, street, postalCode, houseNumber, queryScore
            except requests.exceptions.RequestException as e:
                if attempt == max_attempts - 1:
                    print(f"Error occurred while making the request for '{address}': {e}")
                    return np.nan, np.nan, None, None, None, None, None, None, None, None, None  # Assign NaN to lat and lng, None to other variables on request error

                wait_time = backoff_seconds
                backoff_seconds *= 2
                print(f"Transient error from HERE API for '{address}': {e}. Retrying in {wait_time:.1f}s "
                      f"(attempt {attempt + 1} of {max_attempts}).")
                time.sleep(wait_time)
            except KeyError as e:
                print(f"Error occurred while parsing response JSON for '{address}': {e}")
                return np.nan, np.nan, None, None, None, None, None, None, None, None, None  # Assign NaN to lat and lng, None to other variables on missing key error

        return np.nan, np.nan, None, None, None, None, None, None, None, None, None

    def geocode_addresses(df, api_key,client_name):
        if df is None or df.empty:
            print("The input DataFrame is empty or None")
            return df
        
        # Initialize lists to store results
        pickup_cols = ['Vers.-Str.', 'Vers.-Str.-Nr.', 'Vers.-PLZ', 'Vers.-Ort']
        dropoff_cols = ['Empf.-Str.', 'Empf.-Str.-Nr.', 'Empf.-PLZ', 'Empf.-Ort']

        pickup_results = []
        dropoff_results = []
        address_cache = {}

        def fetch_with_cache(formatted_address: str):
            if formatted_address not in address_cache:
                address_cache[formatted_address] = get_lat_lng_and_more(formatted_address, api_key)
            return address_cache[formatted_address]

        # Load config to determine what addresses from cleaned data are geocoded
        # Not in all cases this is done for all pickup and dropoff locations, 
        #  e.g. when pickup is a defined location and order data does only contain dropoffs.
        # The geocoding config provides a boolean dict for pickup and dropoff 
        ''' "geocoding": 
            {"pickup": False, # stands for the pickup location shall not! be be geocoded
            "dropoff": True # stands for the dropoff location needs to be geocoded
        }'''

        geocoding_config = CONFIG.get(client_name, {}).get("geocoding", {"pickup": True, "dropoff": True})

        # Check if required columns exist before processing
        for cols in [pickup_cols, dropoff_cols]:
            for col in cols:
                if col not in df.columns:
                    print(f"Warning: Column '{col}' not found in DataFrame. Skipping this column for geocoding.")
                    cols.remove(col)  # Remove the missing column from the list

        # Process pickup and dropoff geocoding based on config
        if geocoding_config.get("pickup", False):
            addresses = [", ".join(str(row[col]) for col in pickup_cols if col in df.columns) for _, row in df.iterrows()]
            pickup_results = [fetch_with_cache(f"{address}, Germany") for address in addresses]
            pickup_df = pd.DataFrame(pickup_results, columns=[f'pickup_{col}' for col in ['lat', 'lng', 'id', 'input', 'label', 'countryCode', 'city', 'street', 'postalCode', 'houseNumber', 'queryScore']])
        else:
            pickup_df = pd.DataFrame(columns=[f'pickup_{col}' for col in ['lat', 'lng', 'id', 'input', 'label', 'countryCode', 'city', 'street', 'postalCode', 'houseNumber', 'queryScore']])

        if geocoding_config.get("dropoff", False):
            addresses = [", ".join(str(row[col]) for col in dropoff_cols if col in df.columns) for _, row in df.iterrows()]
            dropoff_results = [fetch_with_cache(f"{address}, Germany") for address in addresses]
            dropoff_df = pd.DataFrame(dropoff_results, columns=[f'dropoff_{col}' for col in ['lat', 'lng', 'id', 'input', 'label', 'countryCode', 'city', 'street', 'postalCode', 'houseNumber', 'queryScore']])
        else:
            dropoff_df = pd.DataFrame(columns=[f'dropoff_{col}' for col in ['lat', 'lng', 'id', 'input', 'label', 'countryCode', 'city', 'street', 'postalCode', 'houseNumber', 'queryScore']])

        # Concatenate original DataFrame with new columns
        df = pd.concat([df.reset_index(drop=True), pickup_df, dropoff_df], axis=1)

        return df

    # Geocode addresses
    df_geocoded = geocode_addresses(df, api_key,client_name)

    return df_geocoded

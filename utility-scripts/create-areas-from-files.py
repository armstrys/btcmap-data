import requests
import json
import os
from btcmap_api_token import BTCMAP_API_TOKEN


# Set the working directory to the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

data_directory = "upload"

# Loop through each file in the directory
for filename in os.listdir(data_directory):
    # Construct the full path to the file
    file_path = os.path.join(data_directory, filename)

    # Check if the item in the directory is a file (not a subdirectory)
    if os.path.isfile(file_path):
        # Read the content of the file
        with open(file_path, "r") as file:
            area_data = json.load(file)  # Load data from the file

        # Define the API URL and headers
        url = "https://api.btcmap.org/areas"
        headers = {
            'Authorization': f'Bearer {BTCMAP_API_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Convert the area_data to JSON payload
        json_payload = json.dumps(area_data)

        # Send the query to the BTC Map API to create the area
        response = requests.post(url, headers=headers, data=json_payload)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Created area from file: {filename}")
        else:
            print(f"Error creating area from file {filename}: {response.text}")

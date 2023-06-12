#codingan ini buat hit api, ambil 
import requests, json
from datetime import datetime, timedelta
from custom_logging import *
file_log=open("log_api.log","a")

# Set up the API URL and API key
url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
api_key = "56d28c0e6e2ac43bd75cd33620fb699b99d38156543ca201d4ca2bf095faf699"

# Calculate the start and end dates for the past month
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=30)

# Convert the dates to ISO format
start_date_iso = start_date.isoformat()
end_date_iso = end_date.isoformat()

# Set up the headers and parameters for the API request
headers = {"X-OTX-API-KEY": api_key}
params = {"modified_since": start_date_iso, "limit": 50}

# Make the API request and retrieve all pages of results
all_pulses = []
page_num = 1
while True:
    print("Processing Page "+str(page_num))
    # Set the page number for the API request
    params["page"] = page_num
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # If the response is not successful, print an error message and break the loop
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break
    
    # Extract the pulses from the response and add them to the list of all pulses
    pulses = response.json()["results"]
    make_log(file_log,f"Hit API Page {str(page_num)}, got {len(pulses)} data\n")
    all_pulses.extend(pulses)
    
    # If there are no more pages of results, break the loop
    if not response.json().get("next"):
        break
    
    # Increment the page number and continue the loop to retrieve the next page of results
    page_num += 1
make_log(file_log,"Hit API Success, Writing file...\n")

sum_file=0
# Print the pulse names and IDs for the past month
for pulse in all_pulses:
    pulse_name = pulse["name"]
    
    pulse_id = pulse["id"]
    # print(f"{pulse_name}: {pulse_id}")
    nama_file="pulse/"+pulse['id']+'.json'
    with open(nama_file, "w", encoding="utf-8") as f:
        json.dump(pulse, f)
    sum_file+=1
make_log(file_log,f"Success writing file, got {str(sum_file)} file\n")
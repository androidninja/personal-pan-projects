import requests
import os
from datetime import datetime

# Firewall credentials and IP
firewall_ip = "10.1.1.1"
api_key = "API key"

# Construct the URL
url = f"https://{firewall_ip}/api/?type=export&category=device-state&key={api_key}"

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Directory and file path for CSV output
output_dir = "m:/pan-files/"
output_file = os.path.join(output_dir, f"Device-State_{firewall_ip}_{current_date}.tgz")

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

# Make the request
response = requests.get(url, verify=False)

# Check if the request was successful
if response.status_code == 200:
    # write the file
    with open(output_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Device State file downloaded successfully, file location: {output_file}")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
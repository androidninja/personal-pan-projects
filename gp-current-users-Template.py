import requests
import csv
import os
from datetime import datetime
from xml.etree import ElementTree

# https://<panorama-or-firewall-IP>/api/?type=keygen&user=<username>&password=<password>


# Firewall credentials and IP
firewall_ip = "firewall MGMT IP"
api_key = "api key"

# Construct the URL
url = f"https://{firewall_ip}/api/?type=op&cmd=<show><global-protect-gateway><current-user></current-user></global-protect-gateway></show>&key={api_key}"

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Directory and file path for CSV output
output_dir = "m:/pan-files/"
output_file = os.path.join(output_dir, f"GP-Current-Users_{current_date}.csv")

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

# Make the request
response = requests.get(url, verify=False)

if response.status_code == 200:
    try:
        xml_root = ElementTree.fromstring(response.content)
        gp_users = xml_root.find('.//result')

        # Open the CSV file for writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Write the header row
            csv_writer.writerow(["Username", "Login Time", "Public IP", "Internal IP", "Region"])

            if gp_users is not None:
                # Iterate through each DHCP lease entry
                for user in gp_users.findall('.//entry'):
                    # Safely retrieve each element or set to 'N/A' if not found
                    username = user.find('username').text if user.find('username') is not None else 'N/A'
                    region = user.find('source-region').text if user.find('source-region') is not None else 'N/A'
                    virtualip = user.find('virtual-ip').text if user.find('virtual-ip') is not None else 'N/A'
                    publicip = user.find('public-ip').text if user.find('public-ip') is not None else 'N/A'
                    logintime = user.find('login-time').text if user.find('login-time') is not None else 'N/A'

                    # Print the parsed information
                    print(f"Username: {username}, Login Time: {logintime}, Public IP: {publicip}, Internal IP: {virtualip}, Source Region: {region}")

                    # Write the data row to CSV
                    # Comment the next two lines to disable writing the xml file
                    csv_writer.writerow([username, logintime, publicip, virtualip, region])
                
                print(f"\nDHCP lease information has been successfully saved to: {output_file}")
            else:
                print("No DHCP lease information found.")
    except ElementTree.ParseError as e:
        print(f"Failed to parse XML: {e}")
else:
    print(f"Failed to retrieve DHCP information, status code: {response.status_code}")
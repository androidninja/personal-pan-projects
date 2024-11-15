import requests
import csv
import os
from datetime import datetime
from xml.etree import ElementTree

# Firewall credentials and IP
firewall_ip = "firewall MGMT IP"
api_key = "api key"

# Construct the URL
url = f"https://{firewall_ip}/api/?type=op&cmd=<show><dhcp><server><lease><interface>all</interface></lease></server></dhcp></show>&key={api_key}"

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Directory and file path for CSV output
output_dir = "m:/pan-files/"
output_file = os.path.join(output_dir, f"dhcp_lease_info_{current_date}.csv")

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Make the request
response = requests.get(url, verify=False)

# Parse the XML response and write to CSV
if response.status_code == 200:
    try:
        xml_root = ElementTree.fromstring(response.content)
        dhcp_leases = xml_root.find('.//result')

        # Open the CSV file for writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Write the header row
            csv_writer.writerow(["IP Address", "MAC Address", "Hostname", "State", "Duration", "Lease Time"])

            if dhcp_leases is not None:
                # Iterate through each DHCP lease entry
                for lease in dhcp_leases.findall('.//entry'):
                    # Safely retrieve each element or set to 'N/A' if not found
                    ip_address = lease.find('ip').text if lease.find('ip') is not None else 'N/A'
                    mac_address = lease.find('mac').text if lease.find('mac') is not None else 'N/A'
                    hostname = lease.find('hostname').text if lease.find('hostname') is not None else 'N/A'
                    state = lease.find('state').text if lease.find('state') is not None else 'N/A'
                    duration = lease.find('duration').text if lease.find('duration') is not None else 'N/A'
                    leasetime = lease.find('leasetime').text if lease.find('leasetime') is not None else 'N/A'

                    # Print the parsed information
                    print(f"IP Address: {ip_address}, MAC: {mac_address}, Hostname: {hostname}, State: {state}, Duration: {duration}, Lease Time: {leasetime}")

                    # Write the data row to CSV
                    csv_writer.writerow([ip_address, mac_address, hostname, state, duration, leasetime])
                
                print(f"\nDHCP lease information has been successfully saved to: {output_file}")
            else:
                print("No DHCP lease information found.")
    except ElementTree.ParseError as e:
        print(f"Failed to parse XML: {e}")
else:
    print(f"Failed to retrieve DHCP information, status code: {response.status_code}")

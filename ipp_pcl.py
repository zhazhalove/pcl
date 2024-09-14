import requests

# Define the printer IP address and IPP endpoint
printer_ip = "192.168.1.31"   # Your printer's IP address
printer_port = "631"          # Default IPP port is 631
ipp_path = "/"                # Based on the IPP report, the endpoint is at the root

# Construct the printer URI
printer_uri = f"http://{printer_ip}:{printer_port}{ipp_path}"

# Create the PCL commands
esc = chr(27)  # Escape character
pcl_commands = f"{esc}&l2Hhello world{esc}%-12345X"

# Convert the PCL commands to bytes for the POST request
pcl_bytes = pcl_commands.encode('ascii')

# IPP request headers
headers = {
    'Content-Type': 'application/vnd.hp-PCL',
    'Expect': '100-continue'  # Some printers require this header
}

# IPP operation ID for Print-Job (0x0002)
operation_id = b'\x00\x02'  # Print-Job operation

# IPP version (1.1)
ipp_version = b'\x01\x01'

# Request ID (arbitrary)
request_id = b'\x00\x00\x00\x01'

# Build the IPP request attributes
attributes = bytearray()

# Operation Attributes Tag
attributes.append(0x01)

# attributes-charset (utf-8)
attributes.extend([
    0x47,                         # Value Tag: charset
    0x00, 0x12,                   # Name Length: 18 bytes
    *b'attributes-charset',       # Name
    0x00, 0x05,                   # Value Length: 5 bytes
    *b'utf-8'                     # Value
])

# attributes-natural-language (en-us)
attributes.extend([
    0x48,                         # Value Tag: naturalLanguage
    0x00, 0x1B,                   # Name Length: 27 bytes
    *b'attributes-natural-language',
    0x00, 0x05,                   # Value Length: 5 bytes
    *b'en-us'                     # Value
])

# printer-uri (printer-uri)
printer_uri_attribute = printer_uri.encode('utf-8')
attributes.extend([
    0x45,                                 # Value Tag: uri
    0x00, 0x0B,                           # Name Length: 11 bytes
    *b'printer-uri',                      # Name
    (len(printer_uri_attribute) >> 8) & 0xFF,  # Value Length (high byte)
    (len(printer_uri_attribute)) & 0xFF,       # Value Length (low byte)
    *printer_uri_attribute                # Value
])

# End of Attributes Tag
attributes.append(0x03)

# Construct the IPP request
ipp_request = ipp_version + operation_id + request_id + attributes + pcl_bytes

# Send the IPP request
try:
    response = requests.post(
        printer_uri,
        headers={'Content-Type': 'application/ipp'},
        data=ipp_request
    )
    
    # Check the response
    if response.status_code == 200:
        print("Print job sent successfully.")
    else:
        print(f"Failed to send the print job. Status code: {response.status_code}")
        print(f"Response: {response.content}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

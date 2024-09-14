import socket

# Define the printer IP address and port 9100
printer_ip = "192.168.1.31"  # Your printer's IP address
printer_port = 9100          # Port 9100 for RAW printing

# Create the PCL commands
esc = chr(27)  # Escape character
pcl_commands = f"{esc}&l2Hhello world{esc}%-12345X"

# Convert the PCL commands to bytes
pcl_bytes = pcl_commands.encode('ascii')

# Create a socket connection to the printer
try:
    with socket.create_connection((printer_ip, printer_port), timeout=10) as sock:
        sock.sendall(pcl_bytes)
    print("Print job sent successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

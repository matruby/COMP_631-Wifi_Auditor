# WIFI AUDITING TOOL 
import subprocess

# Check what network interfaces are in use
ifaces = subprocess.check_output(['iwconfig'])
ifaces_string = ifaces.decode('utf-8')




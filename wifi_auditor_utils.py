#!/usr/bin/python3
# WIFI AUDITOR TOOL FUNCTION FILE
import re 
import subprocess
import sys 

def banner_print(): 
    ''' 
    Prints the WIFI Auditor tool banner 
    '''
    print(""" __     __     __     ______   __        ______     __  __     _____     __     ______   ______     ______    
/\ \  _ \ \   /\ \   /\  ___\ /\ \      /\  __ \   /\ \/\ \   /\  __-.  /\ \   /\__  _\ /\  __ \   /\  == \   
\ \ \/ ".\ \  \ \ \  \ \  __\ \ \ \     \ \  __ \  \ \ \_\ \  \ \ \/\ \ \ \ \  \/_/\ \/ \ \ \/\ \  \ \  __<   
 \ \__/".~\_\  \ \_\  \ \_\    \ \_\     \ \_\ \_\  \ \_____\  \ \____-  \ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_/   \/_/   \/_/   \/_/     \/_/      \/_/\/_/   \/_____/   \/____/   \/_/     \/_/   \/_____/   \/_/ /_/ """)

def options_list():
    ''' 
    Print out a list of options for the users to choose from   
    '''
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def interface_check():
    '''
    Check if there is Wi-Fi capable interfaces
    if there is return a list of there name and 
    operating mode
    '''
    ifaces = subprocess.run(["iwconfig"], capture_output=True, text=True)

    # Checks 
    if ifaces.stdout == "":
        print("!!! CONNECT WIRELESS INTERFACE AND RE-RUN PROGRAM !!!")
        sys.exit()
    
    wlan_iface_info = re.findall(r'(wlan\d+).*?Mode:([^ ]+)', ifaces.stdout, re.DOTALL)
    return wlan_iface_info


banner_print()
options_list()

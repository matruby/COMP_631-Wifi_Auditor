#!/usr/bin/python3
# WIFI AUDITOR TOOL FUNCTION FILE
import re
import subprocess
import sys
import time


class Auditor:
	def __init__(self, iface, iface_mode):
		self.iface = iface
		self.iface_mode = iface_mode

	def interface_check(self):
		'''
		Check if there is Wi-Fi capable interfaces
		if there is return a list of there name and 
		operating mode
		'''
		# Runs the subprocess command to get the output from iwconfig in string format
		ifaces = subprocess.run(["iwconfig"], capture_output=True, text=True)

		# Checks if there is a wifi interface available, if not it will exit
		if ifaces.stdout == "":
			print("!!! CONNECT WIRELESS INTERFACE AND RE-RUN PROGRAM !!!")
			sys.exit()

		# If there a usable interface, get the interface name
		# and the current mode it's operating in.
		wlan_iface_info = re.findall(r'(wlan\d+).*?Mode:([^ ]+)', ifaces.stdout, re.DOTALL)

		return wifi_iface_info    

	def set_interface(self, iface_info):
		'''
		Based on the value passed in by interface_check, 
		help the user set the Wireless Interface they want to 
		use with this tool. 
		'''
		# Checks how many values were passed in
		if len(iface_info) > 1:
			while True:
				print("------------ Mᴜʟᴛɪᴘʟᴇ Iɴᴛᴇʀғᴀᴄᴇs Dᴇᴛᴇᴄᴛᴇᴅ ------------\n")

				# Print out all of the interfaces and their modes 
				counter = 0
				for iface in iface_info:
					wifi_interface = iface[0]
					mode_value = iface[1]
					print(f"{counter}. Wi-Fi Interface: {wifi_interface}, Mode: {mode_value}\n")
					# Increase counter to have a numbered list
					counter += 1

				print("------------------------------------------------------\n")

				# Prompt the user to choose the interface they'd like to use
				print("------------ Cʜᴏᴏsᴇ Dᴇsɪʀᴇᴅ Iɴᴛᴇʀғᴀᴄᴇ (Nᴜᴍʙᴇʀs Oɴʟʏ) ------------\n")
				choice = int(input("--> "))

				# Set the interface values in the class
				if choice > len(iface_info):
					print("Invalid Choice, retry!")
					continue

				else:
					self.iface = iface_info[0][0]
					self.iface_mode = iface_info[0][1]

	def wifi_area_scan(self):
		'''
		Scan for Wi-Fi Networks in the Surrounding Area
		'''
		self.clear_term()
		print("Scanning")

	def wpa2_crack_attack(self):
		'''
		Perform a WPA2 Cracking Attack. 
		1. Set up a listener to catch the EAPOL Packets.
		2. Deauth_the_AP. 
		3. Capture the Packets. 
		4. Run the cracking attack. 
		'''
		self.clear_term()
		print("Cracking...")

	def auth_flood():
		'''
		Perform a Wi-Fi Authentication Flood
		'''
		self.clear_term()
		print("Flooding...")

	def deauth_attack():
		'''
		Perform a Wi-Fi De-Authentication Attack
		'''
		self.clear_term()
		print("Deauthing...")


	def beacon_flood():
		'''
		Perform a Wi-Fi Beacon Flood Attack
		'''
		self.clear_term()
		print("Beacon Flooding...")

	def layer_1_dos():
		'''
		Peform a Layer 1 Denial of Service Attack.
		'''
		self.clear_term()
		print("Spamming...")

	def options_list(self):
		'''
		Print out a list of options for the users to choose from
		'''
		while True:
			self.banner_print()
			print(f"Selected Interface --> {self.iface}")
			print(f"Current Interface Mode --> {self.iface_mode}")
			print("----------------------------------------------------------------------------------")
			print("""
............................... Aᴜᴅɪᴛ Tᴏᴏʟ Lɪsᴛ ...................................

1. Sʜᴏᴡ Wɪ-Fɪ Nᴇᴛᴡᴏʀᴋs ɪɴ ᴛʜᴇ Sᴜʀʀᴏᴜɴᴅɪɴɢ Aʀᴇᴀ
2. Pᴇʀғᴏʀᴍ ᴀ WPA2 Cʀᴀᴄᴋɪɴɢ Aᴛᴛᴀᴄᴋ
3. Aᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ Fʟᴏᴏᴅ (Lᴀʏᴇʀ 2 DᴏS)
4. Dᴇᴀᴜᴛʜ Aᴛᴛᴀᴄᴋ (Lᴀʏᴇʀ 2 DᴏS)
5. Bᴇᴀᴄᴏɴ Fʟᴏᴏᴅ (Lᴀʏᴇʀ 2 DᴏS)
6. Lᴀʏᴇʀ 1 DᴏS
7. Exɪᴛ ᴛʜᴇ Pʀᴏɢʀᴀᴍ
..................................................................................
			""")

			try:
				choice = int(input("-------------------------- Cʜᴏᴏsᴇ ᴀ Tᴏᴏʟ (Nᴜᴍʙᴇʀs Oɴʟʏ) -------------------------- \n--> "))

				if choice == 1 and choice <= 7:
					self.wifi_area_scan()
					break
				elif choice == 2 and choice <= 7:
					self.wpa2_cracking_attack()
					break
				elif choice == 3 and choice <= 7:
					self.auth_flood()
					break
				elif choice == 4 and choice <= 7:
					self.deauth_attack()
					break
				elif choice == 5 and choice <= 7:
					self.beacon_flood()
					break
				elif choice == 6 and choice <= 7:
					self.layer_1_dos()
					break
				elif choice == 7 and choice <= 7:
					sys.exit()
				else:
					self.clear_term()
					print("Number Out of Range, Retry the Option...")
					time.sleep(3)
					continue
			except Exception:
				self.clear_term()
				print("Invalid Option, Retry the Option...")
				time.sleep(3)
				continue

	def clear_term(self):
		'''
		Function to clear the terminal output.
		'''
		subprocess.run(["clear"])

	def banner_print(self):
		'''
		Prints the WIFI Auditor tool banner
		'''
		print("""
     __     __     __     ______   __                                     
    /\ \  _ \ \   /\ \   /\  ___\ /\ \                                    
    \ \ \/ ".\ \  \ \ \  \ \  __\ \ \ \                                   
     \ \__/".~\_\  \ \_\  \ \_\    \ \_\                                  
      \/_/   \/_/   \/_/   \/_/     \/_/                                  
                                                                      
     ______     __  __     _____     __     ______   ______     ______    
    /\  __ \   /\ \/\ \   /\  __-.  /\ \   /\__  _\ /\  __ \   /\  == \   
    \ \  __ \  \ \ \_\ \  \ \ \/\ \ \ \ \  \/_/\ \/ \ \ \/\ \  \ \  __<   
     \ \_\ \_\  \ \_____\  \ \____-  \ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
      \/_/\/_/   \/_____/   \/____/   \/_/     \/_/   \/_____/   \/_/ /_/  
		""")
		print("----------------------------------------------------------------------------------")


wlan0interface = Auditor("wlan0", "Mananged")
wlan0interface.banner_print()
wlan0interface.options_list()

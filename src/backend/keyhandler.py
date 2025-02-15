
r"""
Implements the backend handler that interacts with the key on disk.

\author Bertram Richter, Xiaoli Song
\date 2025
"""


import json
import os
import shutil


class KeyHandler:
	r"""
	Handle keyfile operations related to activation and deactivation, as well as reading keyfiles from directories.
	The KeyHandler manages two directories: one for activated keyfiles and one for deactivated keyfiles.
	It provides methods to check if the directories exist, read keyfiles, and move keyfiles between activated
	and deactivated directories.
	"""
	def __init__(self, activated_path, deactivated_path):
		r"""
		Initialize the KeyHandler with the paths for activated and deactivated directories.
		\param activated_path (str): The file path where activated keyfiles are stored.
		\param deactivated_path (str): The file path where deactivated keyfiles are stored.
		"""
		self.activated_path = activated_path
		self.deactivated_path = deactivated_path
	
	def check_directories(self):
		r"""
		Check if both the activated and deactivated directories exist.
		\return (bool): True if both directories exist, False if one or both do not exist.
		"""
		if not os.path.exists(self.activated_path):
			return False
		if not os.path.exists(self.deactivated_path):
			return False
		return True
	
	def read_keys(self, status):
		r"""
		Read and return a list of serial numbers from userProperties.json files within the folders in
		the specified base directory.
		\param status (str): 'activated' or 'deactivated'. Uses the activated_path or deactivated_path as the base directory.
		\return (list): A list containing all sensorSerialNumber values found in the userProperties.json files.
		"""
		if status == 'activated':
			base_directory = self.activated_path
		else:
			base_directory = self.deactivated_path
		serial_numbers = []
		for folder_name in os.listdir(base_directory):
			folder_path = os.path.join(base_directory, folder_name)
			if os.path.isdir(folder_path):
				json_file_path = os.path.join(folder_path, "userProperties.json")
				if os.path.exists(json_file_path):
					try:
						with open(json_file_path, "r") as json_file:
							data = json.load(json_file)
							sensor_serial_number = data.get("sensorSerialNumber", None)
							if sensor_serial_number:
								serial_numbers.append(sensor_serial_number)
					except json.JSONDecodeError:
						pass
				else:
					pass
		return serial_numbers
	
	def activate_key(self, key_file):
		r"""
		Move a keyfile from the deactivated directory to the activated directory.
		\param key_file (str): The name of the keyfile (without extension) to activate.
		\return (bool): True if the keyfile was successfully moved, False if the file path does not exist.
		"""
		current_path = os.path.join(self.deactivated_path, key_file)
		new_path = os.path.join(self.activated_path, key_file)
		if os.path.exists(current_path):
			shutil.move(current_path, new_path)
			return True
		else:
			return False
	
	def deactivate_key(self, key_file):
		r"""
		Move a keyfile from the activated directory to the deactivated directory.
		\param key_file (str): The name of the keyfile (without extension) to deactivate.
		\return (bool): True if the keyfile was successfully moved, False if the file path does not exist.
		"""
		current_path = os.path.join(self.activated_path, key_file)
		new_path = os.path.join(self.deactivated_path, key_file)
		if os.path.exists(current_path):
			shutil.move(current_path, new_path)
			return True
		else:
			return False
	
	def key_folder_path(self, serial_number, status):
		r"""
		Find the folder path containing the given serial number by searching through the userProperties.json files.
		\param serial_number (str): The serial number to locate.
		\param status (str): 'activated' or 'deactivated' to determine the base directory.
		\return (str): The full folder path containing the specified serial number, or None if not found.
		"""
		if status == 'activated':
			base_directory = self.activated_path
		else:
			base_directory = self.deactivated_path
		for folder_name in os.listdir(base_directory):
			folder_path = os.path.join(base_directory, folder_name)
			if os.path.isdir(folder_path):
				json_file_path = os.path.join(folder_path, "userProperties.json")
				if os.path.exists(json_file_path):
					try:
						with open(json_file_path, "r") as json_file:
							data = json.load(json_file)
							sensor_serial_number = data.get("sensorSerialNumber", None)
							if sensor_serial_number == serial_number:
								return folder_path
					except json.JSONDecodeError:
						pass
		return None

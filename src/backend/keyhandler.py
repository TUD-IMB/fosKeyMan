
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
	def __init__(self, activated_path, deactivated_path, trash_path):
		r"""
		Initialize the KeyHandler with the paths for activated and deactivated directories.
		\param activated_path (str): The file path where activated keyfiles are stored.
		\param deactivated_path (str): The file path where deactivated keyfiles are stored.
		"""
		self.activated_path = activated_path
		self.deactivated_path = deactivated_path
		self.trash_path = trash_path
	
	def check_directories(self):
		r"""
		Check if both the activated and deactivated directories exist.
		\return (bool): True if both directories exist, False if one or both do not exist.
		"""
		if not os.path.exists(self.activated_path):
			return False
		if not os.path.exists(self.deactivated_path):
			return False
		if not os.path.exists(self.trash_path):
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
		elif status == 'deactivated':
			base_directory = self.deactivated_path
		elif status == 'trash':
			base_directory = self.trash_path
		else:
			return
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

	def delete_key(self, key_file):
		r"""
		Move a keyfile from either the activated or deactivated directory into the trash directory.
		\param key_file (str): The folder name of the keyfile to delete.
		\return (bool): True if deleted (moved to trash), False if not found.
		"""
		source_path = None

		if os.path.exists(os.path.join(self.activated_path, key_file)):
			source_path = os.path.join(self.activated_path, key_file)
		elif os.path.exists(os.path.join(self.deactivated_path, key_file)):
			source_path = os.path.join(self.deactivated_path, key_file)

		if not source_path:
			return False

		trash_target = os.path.join(self.trash_path, key_file)

		if os.path.exists(trash_target):
			shutil.rmtree(trash_target)

		shutil.move(source_path, trash_target)
		return True

	def undo_delete_key(self, key_file):
		r"""
		Restore a keyfile from the trash directory to the deactivated directory.
		\param key_file (str): The folder name of the keyfile to restore.
		\return (bool): True if restored, False if not found in trash.
		"""
		trash_path = os.path.join(self.trash_path, key_file)
		restore_path = os.path.join(self.deactivated_path, key_file)

		if not os.path.exists(trash_path):
			return False

		if os.path.exists(restore_path):
			shutil.rmtree(restore_path)

		shutil.move(trash_path, restore_path)
		return True

	def permanently_delete_key(self, key_file):
		r"""
		Permanently delete a keyfile folder from the trash directory.
		\param key_file (str): The folder name of the keyfile to delete.
		\return (bool): True if deleted, False if not found.
		"""
		trash_path = os.path.join(self.trash_path, key_file)

		if os.path.exists(trash_path) and os.path.isdir(trash_path):
			shutil.rmtree(trash_path)
			return True
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

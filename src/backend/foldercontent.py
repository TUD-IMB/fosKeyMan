
r"""
Implements the backend to manage the content sensor keys on disk.

\author Bertram Richter, Xiaoli Song
\date 2025
"""


from datetime import datetime
import os
import json


class FolderContent:
	r"""
	Handle reading JSON files (userProperties.json and gageSegment.json) from keyfile folders located
	in activated or deactivated directories.
	"""
	def __init__(self, activated_path, deactivated_path):
		r"""
		Initialize the FolderContent with paths for activated and deactivated keyfile directories.
		\param activated_path (str): The path to the directory containing activated keyfiles.
		\param deactivated_path (str): The path to the directory containing deactivated keyfiles.
		"""
		self.activated_path = activated_path
		self.deactivated_path = deactivated_path
	
	def read_user_properties(self, key):
		r"""
		Read the content of the userProperties.json file from the specified key's folder.
		The method checks if the key's folder exists in the activated or deactivated directories,
		and attempts to load the 'userProperties.json' file from within the folder.
		\param key (str): The name of the key to locate its corresponding key file folder.
		\return (dict or None): A dictionary containing the parsed JSON data, or None if the file does not exist.
		"""
		keyfile_path_act = os.path.join(self.activated_path, key, 'userProperties.json')
		keyfile_path_deact = os.path.join(self.deactivated_path, key, 'userProperties.json')
		if os.path.exists(keyfile_path_act):
			return self.load_json(keyfile_path_act)
		elif os.path.exists(keyfile_path_deact):
			return self.load_json(keyfile_path_deact)
		else:
			return None
	
	def read_gage_segment(self, key):
		r"""
		Read the content of the gageSegment.json file from the specified key's keyfile folder.
		Similar to `read_user_properties`, this method checks if the key's keyfile folder exists in the activated or
		deactivated directories and attempts to load the 'gageSegment.json' file from within the folder.
		\param key (str): The name of the key to locate its corresponding key file folder.
		\return (dict or None): A dictionary containing the parsed JSON data, or None if the file does not exist.
		"""
		keyfile_path_act = os.path.join(self.activated_path, key, 'gageSegment.json')
		keyfile_path_deact = os.path.join(self.deactivated_path, key, 'gageSegment.json')
		if os.path.exists(keyfile_path_act):
			return self.load_json(keyfile_path_act)
		elif os.path.exists(keyfile_path_deact):
			return self.load_json(keyfile_path_deact)
		else:
			return None
	
	def read_od6ref_file(self, key):
		r"""
		Read the first line of the .od6ref file from the specified key's keyfile folder.
		\param key (str): The name of the key to locate its corresponding folder.
		\return (dict or None): A dictionary containing the parsed JSON data, or None if the file does not exist.
		"""
		keyfile_path_act = os.path.join(self.activated_path, key, f'{key}.od6ref')
		keyfile_path_deact = os.path.join(self.deactivated_path, key, f'{key}.od6ref')
		if os.path.exists(keyfile_path_act):
			return self.load_json(keyfile_path_act)
		elif os.path.exists(keyfile_path_deact):
			return self.load_json(keyfile_path_deact)
		else:
			return None
	
	def load_json(self, file_path):
		r"""
		Load and parse a JSON file from within a key file.
		\param file_path (str): The path to the JSON or binary file.
		\return (dict or None): A dictionary containing the parsed JSON data, or None if the file could not be read.
		"""
		try:
			with open(file_path, 'rb') as file:
				# data = json.load(file)
				# return data
				first_line = file.readline().strip()
				return json.loads(first_line)
		except json.JSONDecodeError:
			return None
		except Exception as e:
			print(f"Error reading JSON from {file_path}: {e}")
			return None
	
	def full_text_search(self, search_term, keyfile=None):
		r"""
		Full-text search inside all JSON files.
		\param search_term (str): The term to search within the JSON files.
		\param keyfile (str or None): The specific key for keyfile to search within. If None, search in all keyfile folders.
		\return (list of tuples): A list of (keyfile name, matching content) tuples where the search term was found.
		"""
		results = []
		for directory in [self.activated_path, self.deactivated_path]:
			if not os.path.exists(directory):
				continue
			if keyfile:
				folder_path = os.path.join(directory, keyfile)
				if os.path.exists(folder_path) and os.path.isdir(folder_path):
					result = self.search_in_folder(folder_path, search_term)
					if result:
						results.append(result)
				continue
			for folder_name in os.listdir(directory):
				folder_path = os.path.join(directory, folder_name)
				if os.path.isdir(folder_path):
					result = self.search_in_folder(folder_path, search_term)
					if result:
						results.append(result)
		return results
	
	def search_in_folder(self, folder_path, search_term):
		r"""
		Search inside a key file folder for the given search term in the JSON files.
		\param folder_path (str): The path to the key file.
		\param search_term (str): The term to search for.
		\return (tuple or None): The serial number and matching content if the search term is found, None otherwise.
		"""
		try:
			keyfile = os.path.basename(folder_path)
			all_matches = []
			for file_name in os.listdir(folder_path):
				if file_name.endswith(".json"):
					file_path = os.path.join(folder_path, file_name)
					with open(file_path, 'r', encoding='utf-8') as file:
						try:
							data = json.load(file)
							result = self.search_in_json(data, search_term)
							if result:
								all_matches.extend(result)
						except json.JSONDecodeError:
							continue
			if all_matches:
				return keyfile, all_matches
		except Exception as e:
			print(f"Error reading folder {folder_path}: {e}")
		return None

	def search_in_json(self, data, search_term):
		r"""
		Recursively search through a JSON for the search term, case-insensitive, with partial matching.
		\param data (dict or list): The JSON data to search through.
		\param search_term (str): The term to search for.
		\return (list): A list of matching key-value pairs if the search term is found, otherwise an empty list.
		"""
		search_term_lower = search_term.lower()
		matches = []
		if isinstance(data, dict):
			for key, value in data.items():
				key_str = str(key).lower()
				if search_term_lower in key_str:
					matches.append({key: value})
				if isinstance(value, (str, int, float, bool)):
					value_str = str(value).lower()
					if search_term_lower in value_str:
						matches.append({key: value})
				elif isinstance(value, (dict, list)):
					matches.extend(self.search_in_json(value, search_term))
		elif isinstance(data, list):
			for item in data:
				matches.extend(self.search_in_json(item, search_term))
		return matches
	
	def get_last_edit_date(self, key):
		r"""
		Retrieve the lastEditDate from the userProperties.json file of the specified key's ZIP file.
		\param key (str): The name of the key to locate its corresponding ZIP file.
		\return (datetime or None): The lastEditDate as a datetime object, or None if not found or not valid.
		"""
		user_properties = self.read_user_properties(key)
		if user_properties:
			last_edit_date_str = user_properties.get('lastEditDate')
			if last_edit_date_str:
				try:
					return datetime.strptime(last_edit_date_str, "%a %b %d %Y")
				except ValueError as e:
					print(f"Error parsing date: {e}")
					return None
		return None
	
	def read_sensor_name_for_key(self, key):
		r"""
		Read the userSensorName from the userProperties.json file in the specified key's folder.
		\param key (str): The name of the key to locate its corresponding folder.
		\return (str or None): The value of userSensorName if it exists, or None otherwise.
		"""
		user_properties = self.read_user_properties(key)
		if user_properties:
			return user_properties.get("userSensorName", None)
		else:
			return None
	
	def edit_sensor_name_for_key(self, key, new_sensor_name):
		r"""
		Edit the userSensorName for a specified key in the userProperties.json file and synchronize the lastEditDate.
		\param key (str): The key whose userSensorName needs to be updated.
		\param new_sensor_name (str): The new sensor name to set.
		\return (bool): True if the update was successful, False otherwise.
		"""
		keyfile_path_act = os.path.join(self.activated_path, key, 'userProperties.json')
		keyfile_path_deact = os.path.join(self.deactivated_path, key, 'userProperties.json')
		json_file_path = keyfile_path_act if os.path.exists(keyfile_path_act) else keyfile_path_deact
		if not json_file_path:
			print(f"No userProperties.json found for key: {key}")
			return False
		try:
			with open(json_file_path, 'r', encoding='utf-8') as file:
				first_line = file.readline().strip()
			user_properties = json.loads(first_line)
			user_properties["userSensorName"] = new_sensor_name
			user_properties["lastEditDate"] = datetime.now().strftime("%a %b %d %Y")
			with open(json_file_path, 'w', encoding='utf-8') as file:
				file.write(json.dumps(user_properties, ensure_ascii=False))
			return True
		except (json.JSONDecodeError, IOError) as e:
			return False

	def read_sensor_length_for_key(self, key):
		r"""
		Read the "sensorLength (m)" value from the .od6ref file in the specified key's folder.
		\param key (str): The name of the key to locate its corresponding folder.
		\return (float or None): The value of "sensorLength (m)" if it exists, or None otherwise.
		"""
		od6ref_data = self.read_od6ref_file(key)
		if od6ref_data:
			return od6ref_data.get("sensorDataProcParams", {}).get("sensorLength (m)", None)
		else:
			return None

	def read_metadata(self, key):
		"""
		Read the content of the metadata.json file from the specified key's folder.
		The method checks if the key's folder exists in the activated or deactivated directories,
		and attempts to load the 'metadata.json' file from within the folder.

		:param key: The name of the key to locate its corresponding key file folder.
		:return: A dictionary containing the parsed JSON data, or an empty dict if the file does not exist.
		"""
		keyfile_path_act = os.path.join(self.activated_path, key, "metadata.json")
		keyfile_path_deact = os.path.join(self.deactivated_path, key, "metadata.json")

		file_path = keyfile_path_act if os.path.exists(keyfile_path_act) else keyfile_path_deact
		if file_path and os.path.exists(file_path):
			try:
				with open(file_path, "r", encoding="utf-8") as file:
					return json.load(file)
			except json.JSONDecodeError:
				print(f"Error: Could not decode JSON in {file_path}")
				return {}
		return {}

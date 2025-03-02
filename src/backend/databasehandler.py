
r"""
Implements the backend handler that interacts with the data base.

\author Bertram Richter, Xiaoli Song
\date 2025
"""


import os
import sqlite3
import zipfile
import io


class DatabaseHandler:
	r"""
	This class provides methods for interacting with the database, including keyfile management (storing as BLOBs),
	as well as basic CRUD (Create, Read, Update, Delete) operations on the 'keytable'.
	"""
	def __init__(self, db_path):
		r"""
		Initialize the DatabaseHandler with the path to the SQLite database.
		\param db_path (str): The path to the SQLite database file.
		"""
		self.db_path = db_path
		self.connection = None
		self.cursor = None
	
	def connect(self):
		r"""Connect to the SQLite database and initialize the cursor."""
		self.connection = sqlite3.connect(self.db_path)
		self.cursor = self.connection.cursor()
	
	def close(self):
		r"""Close the database connection and reset the cursor."""
		if self.connection:
			self.connection.close()
			self.connection = None
			self.cursor = None
	
	def rollback(self):
		r"""Rollback the current transaction in case of an error."""
		self.connection.rollback()
	
	def create_table(self):
		r"""Create the default 'keytable' when new a database."""
		create_table_query = """
			CREATE TABLE IF NOT EXISTS keytable (
			serial_number TEXT PRIMARY KEY,
			name TEXT,
			project TEXT,
			operator TEXT,
			specimen TEXT,
			dfos_type TEXT,
			installation TEXT,
			notes TEXT,
			keyfile BLOB
		)
		"""
		try:
			self.cursor.execute(create_table_query)
			self.connection.commit()
			print("Table 'keytable' created successfully.")
		except sqlite3.Error as e:
			# print(f"Failed to create table: {e}")
			raise e
	
	def insert_data(self, row_data):
		r"""
		Insert a new record into the 'keytable'.
		\param row_data (tuple): A tuple containing the values for each column in the table.
		"""
		placeholders = ','.join(['?'] * len(row_data))
		sql = f"INSERT INTO keytable VALUES ({placeholders})"
		self.cursor.execute(sql, row_data)
	
	def delete_data(self, serial_number):
		r"""
		Delete a record from 'keytable' based on the serial_number.
		\param serial_number (str): The serial number of the record to delete.
		"""
		self.cursor.execute("DELETE FROM keytable WHERE serial_number=?", (serial_number,))
	
	def update_data(self, row_data):
		r"""
		Update an existing record in 'keytable' (for table content modification).
		\param row_data (tuple): A tuple containing the updated values for each column in the table.
		"""
		columns = ['serial_number', 'name', 'project', 'operator', 'specimen', 'dfos_type', 'installation', 'notes']
		serial_number = row_data[0]
		set_clause = ', '.join(f"{col}=?" for col in columns if col != 'serial_number')
		sql = f"UPDATE keytable SET {set_clause} WHERE serial_number=?"
		update_values = row_data[1:]
		update_values.append(serial_number)
		self.cursor.execute(sql, update_values)
	
	def update_name(self, serial_number, new_name):
		r"""
		Update the sensor name for a specific serial number in the database.
		\param serial_number (str): The serial number of the record to update.
		\param new_name (str): The new sensor name to update.
		"""
		sql = "UPDATE keytable SET name=? WHERE serial_number=?"
		self.cursor.execute(sql, (new_name, serial_number))
	
	def fetch_all_data(self):
		r"""
		Fetch all records from 'keytable'.
		\return (list): A list of all records in the table.
		"""
		self.cursor.execute("SELECT * FROM keytable")
		return self.cursor.fetchall()
	
	def commit(self):
		r"""Commit the transaction to the database."""
		self.connection.commit()
	
	def get_all_data_dict(self):
		r"""
		Retrieve all records from the database and return them as a dictionary keyed by serial_number.
		\return: dict A dictionary where the key is the serial_number and the value is the corresponding row data.
		"""
		self.cursor.execute("SELECT * FROM keytable")
		rows = self.cursor.fetchall()
		data_dict = {}
		for row in rows:
			serial_number = row[0]
			data_dict[serial_number] = row
		return data_dict
	
	def key_exists_in_keyfile(self, key):
		r"""
		Check if the keyfile column for the given serial_number contains data, used for keyfile status check when table setup.
		\param key (str): The serial number of the record to check.
		\return (bool): True if keyfile contains data, otherwise False.
		"""
		self.cursor.execute(
			"SELECT COUNT(1) FROM keytable WHERE serial_number = ? AND keyfile IS NOT NULL AND keyfile != ''",
			(key,)
		)
		result = self.cursor.fetchone()
		return result[0] > 0
	
	def key_exists_in_database(self, key):
		r"""
		Check if the given serial_number exists record in the database.
		\param key (str): The serial number to check for existence.
		\return (bool): True if the serial_number exists, otherwise False.
		"""
		self.cursor.execute("SELECT COUNT(1) FROM keytable WHERE serial_number = ?", (key,))
		result = self.cursor.fetchone()
		return result[0] > 0
	
	def read_keys(self):
		r"""
		Read all serial_number values from the 'keytable'.
		\return: list A list of all serial numbers from the table.
		"""
		self.cursor.execute("SELECT serial_number FROM keytable")
		keys = [row[0] for row in self.cursor.fetchall()]
		return keys
	
	def get_key_details(self, key):
		r"""
		Retrieve all details for a given serial_number from the 'keytable'.
		\param key (str): The serial number of the record to retrieve.
		\return (tuple): A tuple containing all column values for the given serial_number.
		"""
		self.cursor.execute("""
			SELECT serial_number, name, project, operator, specimen, dfos_type, installation, notes, keyfile
			FROM keytable
			WHERE serial_number = ?
		""", (key,))
		return self.cursor.fetchone()
	
	def update_blob_data(self, blob_data, serial_number):
		r"""
		Update the keyfile column with BLOB data directly for the given serial_number.

		\param blob_data (bytes): The BLOB data to be written to the database.
		\param serial_number (str): The serial number of the record to update.
		"""
		try:
			self.cursor.execute("UPDATE keytable SET keyfile = ? WHERE serial_number = ?", (blob_data, serial_number))
		except Exception as e:
			print(f"An error occurred: {e}")
			self.rollback()
	
	def get_blob_data(self, serial_number):
		r"""
		Retrieve the BLOB data (keyfile) for a given serial_number.
		\param serial_number (str): The serial number of the record to retrieve the BLOB.
		\return (bytes or None): The BLOB data if found, otherwise None.
		"""
		try:
			self.cursor.execute("SELECT keyfile FROM keytable WHERE serial_number = ?", (serial_number,))
			blob_data = self.cursor.fetchone()
			if blob_data:
				return blob_data[0]
			else:
				# print("No data found for the given serial number.")
				return None
		except Exception as e:
			print(f"An error occurred: {e}")
			self.rollback()
			return None

	def remove_blob_data(self, serial_number):
		r"""
		Set the BLOB data (keyfile) to NULL for a given serial_number
		\param serial_number (str): The serial number whose keyfile should be removed.
		"""
		try:
			self.cursor.execute("UPDATE keytable SET keyfile = NULL WHERE serial_number = ?", (serial_number,))
		except Exception as e:
			self.rollback()

	def fetch_blob_and_save_as_folder(self, serial_number, output_folder_path):
		r"""
		Fetch the BLOB data from the database and save it as a folder.
		\param serial_number (str): The serial number of the record containing the BLOB data.
		\param output_folder_path (str): The path where the folder will be saved.
		"""
		try:
			self.cursor.execute("SELECT keyfile FROM keytable WHERE serial_number = ?", (serial_number,))
			blob_data = self.cursor.fetchone()
			if blob_data:
				os.makedirs(output_folder_path, exist_ok=True)
				with zipfile.ZipFile(io.BytesIO(blob_data[0]), 'r') as zip_file:
					zip_file.extractall(output_folder_path)
				print("Folder has been saved successfully.")
			else:
				print("No data found for the given serial number.")
		except Exception as e:
			print(f"An error occurred: {e}")
			self.rollback()
	
	def create_zip_from_folder(self, folder_path):
		r"""
		Create a ZIP from the given folder.
		\param folder_path (str): Path to the folder to zip.
		\return (BytesIO): The binary ZIP data.
		"""
		zip_buffer = io.BytesIO()
		with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
			for root, dirs, files in os.walk(folder_path):
				for file in files:
					file_path = os.path.join(root, file)
					arcname = os.path.relpath(file_path, start=folder_path)
					zipf.write(file_path, arcname)
		zip_buffer.seek(0)
		return zip_buffer

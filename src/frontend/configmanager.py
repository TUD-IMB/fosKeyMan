import json
import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox


class ConfigManager(QObject):
	r"""
	Manage the loading, saving, and validation of configuration settings for directories and database paths.
	Language setting for the user interface (e.g., 'english' or 'german').
	Handle user interaction for selecting directories and database paths, and ensures that the configuration is
	correctly loaded from and saved to a JSON file.
	"""
	def __init__(self, config_path):
		r"""
		Initialize the ConfigManager with the path to the configuration file.

		\param config_path (str): The file path where the configuration is stored.
		"""
		super(ConfigManager, self).__init__()
		self.config_path = config_path
		self.directory1 = None
		self.directory2 = None
		self.db_path = None
		self.language = None
		self.config = self.load_config()

	def create_default_config(self):
		r"""
		Create a default configuration file. Default language is English.

		\return (dict): The default configuration.
		"""
		default_config = {
			'directory1': '',
			'directory2': '',
			'db_path': '',
			'language': 'english'
		}
		with open(self.config_path, 'w') as f:
			json.dump(default_config, f)
		return default_config

	def load_config(self):
		r"""
		Load the configuration file. If it doesn't exist or has errors, return an empty configuration.

		\return (dict): The loaded configuration as a dictionary, or the default dictionary if the file contains errors.
		"""
		if os.path.exists(self.config_path):
			try:
				with open(self.config_path, 'r') as f:
					return json.load(f)
			except json.JSONDecodeError:
				return self.create_default_config()
		else:
			return self.create_default_config()

	def save_config(self):
		r"""
		Save the current directory paths to the configuration file.
		"""
		config_data = {
			'directory1': self.directory1,
			'directory2': self.directory2,
			'db_path': self.db_path,
			'language': self.language
		}
		with open(self.config_path, 'w') as f:
			json.dump(config_data, f)

	def save_db_path(self, db_path):
		r"""
		Save the current database path to the configuration file.

		\param db_path (str): The path to the database file to save.
		"""
		self.db_path = db_path
		config_data = self.load_config()
		config_data['db_path'] = self.db_path

		with open(self.config_path, 'w') as f:
			json.dump(config_data, f)

	def check_and_load_previous_config(self):
		r"""
		Load and check if previously saved directory and database paths are valid.

		\return (tuple): directory1, directory2, db_path, language
		"""
		dir1 = self.config.get('directory1', None)
		dir2 = self.config.get('directory2', None)
		db_path = self.config.get('db_path', None)
		language = self.config.get('language', 'english')

		if dir1 and os.path.exists(dir1):
			self.directory1 = dir1

		if dir2 and os.path.exists(dir2):
			self.directory2 = dir2

		if db_path and os.path.exists(db_path):
			self.db_path = db_path

		if language in ('english', 'german'):
			self.language = language
		else:
			self.language = 'english'

		return self.directory1, self.directory2, self.db_path, self.language

	def select_directory1(self, dialog, open_ui):
		r"""
		Open a file dialog for the user to select the first (activated keyfile) directory.

		\param dialog (QDialog): The dialog window that allows the user to select directories.
		\param open_ui (QWidget): The UI that contains the directory input fields.
		"""
		dir1 = QFileDialog.getExistingDirectory(dialog, self.tr("Please select the activation key file directory"))
		if dir1:
			self.directory1 = dir1
			open_ui.acLineEdit.setText(dir1)

	def select_directory2(self, dialog, open_ui):
		r"""
		Open a file dialog for the user to select the second (deactivated keyfile) directory.

		\param dialog (QDialog): The dialog window that allows the user to select directories.
		\param open_ui (QWidget): The UI that contains the directory input fields.
		"""
		dir2 = QFileDialog.getExistingDirectory(dialog, self.tr("Please select the deactivation key file directory"))
		if dir2:
			self.directory2 = dir2
			open_ui.deacLineEdit.setText(dir2)

	def select_db_path(self, dialog, open_ui):
		r"""
		Open a dialog for the user to select the database file.

		\param dialog (QDialog): The dialog window that allows the user to select directories.
		\param open_ui (QWidget): The UI that contains the directory input fields.
		"""
		db, _ = QFileDialog.getOpenFileName(dialog, self.tr("Select Database File"), "", "Database Files (*.sqlite *.db)")
		if db:
			self.db_path = db
			open_ui.dbLineEdit.setText(db)

	def confirm_directory_selection(self, dialog, open_ui):
		r"""
		Confirm the directory and database selection made by the user.
		Validate that both directories and the database file exist, and close the dialog if valid.

		\param dialog (QDialog): The dialog window that allows the user to select directories.
		\param open_ui (QWidget): The UI that contains the directory input fields.
		"""
		dir1 = open_ui.acLineEdit.text().strip()
		dir2 = open_ui.deacLineEdit.text().strip()
		db = open_ui.dbLineEdit.text().strip()

		if not dir1 or not os.path.exists(dir1):
			QMessageBox.warning(dialog, self.tr("Error"),
								self.tr("Please select a valid directory for activated keyfiles."))
			return
		if not dir2 or not os.path.exists(dir2):
			QMessageBox.warning(dialog, self.tr("Error"),
								self.tr("Please select a valid directory for deactivated keyfiles."))
			return
		if not db or not os.path.exists(db):
			QMessageBox.warning(dialog, self.tr("Error"), self.tr("Please select a valid database."))
			return

		dialog.accept()

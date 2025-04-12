import json
import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox


class ConfigManager(QObject):
	r"""
	Manage the loading, saving, and validation of configuration settings for directories.
	Language setting for the user interface (e.g., 'english' or 'german').
	Handle user interaction for selecting directories, and ensures that the configuration is
	correctly loaded from and saved to a JSON file.
	"""
	DEFAULT_COLUMNS = ["Project", "Operator", "Specimen", "DFOS_Type", "Installation", "Note"]

	def __init__(self, config_path):
		r"""
		Initialize the ConfigManager with the path to the configuration file.

		\param config_path (str): The file path where the configuration is stored.
		"""
		super(ConfigManager, self).__init__()
		self.config_path = config_path
		self.directory1 = None
		self.directory2 = None
		self.language = None
		self.custom_columns = None
		self.config = self.load_config()

	def create_default_config(self):
		r"""
		Create a default configuration file. Default language is English.

		\return (dict): The default configuration.
		"""
		default_config = {
			'directory1': '',
			'directory2': '',
			'language': 'english',
			'custom_columns': self.DEFAULT_COLUMNS
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
			'language': self.language,
			'custom_columns': self.custom_columns
		}
		with open(self.config_path, 'w') as f:
			json.dump(config_data, f)

	def check_and_load_previous_config(self):
		r"""
		Load and check if previously saved directories are valid.

		\return (tuple): directory1, directory2, language
		"""
		dir1 = self.config.get('directory1', None)
		dir2 = self.config.get('directory2', None)
		language = self.config.get('language', 'english')
		columns = self.config.get('custom_columns', self.DEFAULT_COLUMNS)

		if dir1 and os.path.exists(dir1):
			self.directory1 = dir1

		if dir2 and os.path.exists(dir2):
			self.directory2 = dir2

		if language in ('english', 'german'):
			self.language = language
		else:
			self.language = 'english'

		if isinstance(columns, list) and all(isinstance(col, str) for col in columns):
			self.custom_columns = columns
		else:
			self.custom_columns = self.DEFAULT_COLUMNS

		return self.directory1, self.directory2, self.language, self.custom_columns

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

	def confirm_directory_selection(self, dialog, open_ui):
		r"""
		Confirm the directory selection made by the user.
		Validate that both directories exist, and close the dialog if valid.

		\param dialog (QDialog): The dialog window that allows the user to select directories.
		\param open_ui (QWidget): The UI that contains the directory input fields.
		"""
		dir1 = open_ui.acLineEdit.text().strip()
		dir2 = open_ui.deacLineEdit.text().strip()

		if not dir1 or not os.path.exists(dir1):
			QMessageBox.warning(dialog, self.tr("Error"),
								self.tr("Please select a valid directory for activated keyfiles."))
			return
		if not dir2 or not os.path.exists(dir2):
			QMessageBox.warning(dialog, self.tr("Error"),
								self.tr("Please select a valid directory for deactivated keyfiles."))
			return

		# self.custom_columns = self.DEFAULT_COLUMNS

		dialog.accept()

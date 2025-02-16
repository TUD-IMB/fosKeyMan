
r"""
Defines the main Graphical User Interface.

\author Xiali Song, Bertram Richter
\date 2025
"""

import hashlib
import io
import logging
import shutil
import sqlite3
import sys
import os
import json
import tempfile
import time
import webbrowser
import zipfile

from PySide6.QtGui import QIcon, QColor, QBrush
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QStyle, QMessageBox, QTableWidgetItem, QHeaderView, QDialog, \
	QFileDialog, QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtCore import QTranslator, Qt, QCoreApplication, QSize

from frontend.renamesensor import RenameSensor
from frontend.ui.uimain import Ui_MainWindow
from backend.keyhandler import KeyHandler
from backend.databasehandler import DatabaseHandler
from backend.foldercontent import FolderContent
from frontend.configmanager import ConfigManager
from frontend.hoverinfo import HoverInfo
from frontend.tableoperator import TableOperator
from frontend.keyfilereplace import KeyfileReplace
from frontend.keystatus import DBStatus, ActivationStatus
from frontend.ui.uiopen import Ui_Open
from frontend.databasemerger import DatabaseMerger
from utils.utils import format_json_to_html

logging.basicConfig(
	filename='fosKeyManOperation.log',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)


class MainWindow(QMainWindow):
	r"""
	Main User Interface for the application.

	This class represents the main window of the application, which includes setting up the UI, loading configurations,
	initializing handlers, setting up the table, and connecting various actions for user interaction.
	"""
	def __init__(self):
		super().__init__()
		
		# ui_file_path = os.path.join(os.path.dirname(__file__), '../resources/ui', 'main.ui')
		# ui_file = QFile(ui_file_path)
		# ui_file.open(QFile.ReadOnly)
		# self.ui = QUiLoader().load(ui_file)
		# ui_file.close()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.directory1 = None
		self.directory2 = None
		self.db_path = None
		self.key_handler = None
		self.folder_content = None
		self.db_handler = None
		self.config_manager = ConfigManager(file_path('fosKeyManConfig.json'))
		self.directory1, self.directory2, self.db_path, self.language = self.config_manager.check_and_load_previous_config()
		self.translator = QTranslator(self)
		self.table_operator = TableOperator(self.ui.tableWidget)
		self.connect_actions()
		# hover explanation to keyfile. db status and possible operations
		self.hover_info = HoverInfo(self.ui.tableWidget, self)
		# tool action enable or disable
		# self.tool_manager = ToolManager(self.ui.tableWidget, self.ui.actionNew, self.ui.actionDelete,
		# 								self.ui.actionSaveChange,
		# 								self.ui.actionImport, self.ui.actionAttach, self.ui.actionReplace,
		# 								self.ui.actionCopy)
		self.ui.tableWidget.cellClicked.connect(self.table_cell_info)
		self.ui.searchPushButton.clicked.connect(self.execute_search)
		self.setWindowIcon(QIcon(resource_path('resources/foskeyman_logo_short.svg')))
		self.adjust_window_size()

	def adjust_window_size(self):
		r"""
		Dynamically adapts window size to available screen space.
		"""
		screen = self.screen()
		screen_size = screen.availableGeometry()

		width = int(screen_size.width() * 0.7)
		height = int(screen_size.height() * 0.6)

		self.resize(width, height)

	def show_and_check_config(self):
		r"""
		Show the main window and check the configuration. Switch the language based on the saved configuration.
		
		If all required paths (directory1, directory2, db_path) are valid, it will set up the table.
		If any of the paths are missing, it will open the setting dialog for the user to initialize the configuration.
		"""
		# self.ui.show()
		self.show()
		self.switch_language(self.language)
		if self.directory1 and self.directory2 and self.db_path:
			self.initialize_handlers()
			self.setup_table()
		else:
			self.open_setting_dialog()
	
	def connect_actions(self):
		r"""
		Connect UI actions to corresponding methods.
		"""
		# actions for switch language
		self.ui.actionEnglish.triggered.connect(lambda: self.switch_language('english'))
		self.ui.actionGerman.triggered.connect(lambda: self.switch_language('german'))
		# actions for table setup (open directory, new database, connect database)
		self.ui.actionOpen.triggered.connect(self.open_setting_dialog)
		self.ui.actionNewDatabase.triggered.connect(self.new_database_dialog)
		self.ui.actionConnectDatabase.triggered.connect(self.connect_database)
		self.ui.actionImportDatabase.triggered.connect(self.merge_database)
		# activate, deactivate, select all actions
		self.ui.actionActive.triggered.connect(self.toggle_activation)
		self.ui.actionDeactive.triggered.connect(self.toggle_deactivation)
		self.ui.actionSelectAll.triggered.connect(self.table_operator.check_all_boxes)
		# actions for right side tool widget
		self.ui.actionFilter.triggered.connect(self.open_filter_widget)
		self.ui.actionInformation.triggered.connect(self.open_info_widget)
		self.ui.filterDockWidget.visibilityChanged.connect(self.ui.actionFilter.setChecked)
		self.ui.infoDockWidget.visibilityChanged.connect(self.ui.actionInformation.setChecked)
		self.ui.stateComboBox.addItems([self.tr("All"),self.tr("Activated"),self.tr("Deactivated"),self.tr("Unknown")])
		self.ui.stateComboBox.setCurrentText("All")
		self.ui.filterButton.clicked.connect(
			lambda: self.table_operator.filter_table(
				self.ui.serialNumberLineEdit,
				self.ui.nameLineEdit,
				self.ui.projectLineEdit,
				self.ui.operatorLineEdit,
				self.ui.specimenLineEdit,
				self.ui.dFOS_TypeLineEdit,
				self.ui.keyfileLineEdit,
				self.ui.stateComboBox
			)
		)
		self.ui.cancelButton.clicked.connect(
			lambda: self.table_operator.reset_filter(
				self.ui.serialNumberLineEdit,
				self.ui.nameLineEdit,
				self.ui.projectLineEdit,
				self.ui.operatorLineEdit,
				self.ui.specimenLineEdit,
				self.ui.dFOS_TypeLineEdit,
				self.ui.keyfileLineEdit
			)
		)
		self.ui.actionSearch.triggered.connect(self.open_search_widget)
		self.ui.searchDockWidget.visibilityChanged.connect(self.ui.actionSearch.setChecked)
		# actions for database operations (refresh, add row, delete row, save change)
		self.ui.actionRefresh.triggered.connect(self.setup_table)
		self.ui.actionNew.triggered.connect(self.table_operator.add_new_row)
		self.ui.actionDelete.triggered.connect(self.table_operator.delete_row)
		self.ui.actionSaveChange.triggered.connect(self.upload_changes_db)
		# actions for keyfile operations (import, attach, replace, copy)
		self.ui.actionImport.triggered.connect(self.import_keyfile_to_db)
		self.ui.actionAttach.triggered.connect(self.attach_keyfile_to_db)
		self.ui.actionReplace.triggered.connect(self.replace_keyfile_db_disk)
		self.ui.actionCopy.triggered.connect(self.copy_keyfile_to_disk)
		self.ui.actionQuickImport.triggered.connect(self.quick_import_keyfile)
		self.ui.actionRenameSensor.triggered.connect(self.rename_sensor_name)
		self.ui.actionUpdateDBKeyfile.triggered.connect(self.update_db_attached_keyfile)
		# actions for application exit
		self.ui.actionExit.triggered.connect(self.exit_application)
		self.ui.actionDocumentation.triggered.connect(self.open_documentation)
		self.ui.actionUSBLoad.triggered.connect(self.keyfile_transfer)
		self.ui.actionAbout.triggered.connect(self.show_about_dialog)
	
	def show_about_dialog(self):
		r"""
		Open a dialog displaying information about the software.
		"""
		default_info = {
			"version": "Unknown",
			"release_date": "Unknown"
		}
		try:
			with open(resource_path('resources/about.json'), 'r', encoding='utf-8') as file:
				info = json.load(file)
		except (FileNotFoundError, json.JSONDecodeError):
			info = default_info
		version = info.get("version", default_info["version"])
		release_date = info.get("release_date", default_info["release_date"])
		dialog = QDialog(self)
		dialog.setWindowTitle("About")
		dialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
		layout = QVBoxLayout(dialog)
		svg_logo = QSvgWidget(resource_path('resources/foskeyman_logo_long.svg'))
		layout.addWidget(svg_logo, alignment=Qt.AlignCenter)
		info_label = QLabel(f"Version: {version}\nRelease Date: {release_date}")
		info_label.setAlignment(Qt.AlignCenter)
		layout.addWidget(info_label)
		author_label = QLabel(f"Authors:\nBertram Richter\nXiaoli Song")
		author_label.setAlignment(Qt.AlignCenter)
		layout.addWidget(author_label)
		copyright_label = QLabel(f"Copyright:\nInstitut für Massivbau\nTechnische Universität Dresden")
		copyright_label.setAlignment(Qt.AlignCenter)
		layout.addWidget(copyright_label)
		license_label = QLabel(
			"License:\nThis software is licensed under the GNU General Public License (GPL) Version 3, 29  June  2007."
			)
		license_label.setAlignment(Qt.AlignCenter)
		license_label.setWordWrap(True)
		layout.addWidget(license_label)
		dialog.setLayout(layout)
		dialog.exec_()
	
	def keyfile_transfer(self):
		r"""
		Exchange keys with external media.
		Allow user to select a source directory and transfer all keyfile folders to the default deactivated directory.
		Check conflicts in both activated and deactivated directories and handles them based on user selection (overwrite or skip).
		"""
		source_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Transfer")
		if source_dir:
			try:
				for item_name in os.listdir(source_dir):
					source_path = os.path.join(source_dir, item_name)
					check_path_dir2 = os.path.join(self.directory2, item_name)
					check_path_dir1 = os.path.join(self.directory1, item_name)
					final_target_path = os.path.join(self.directory2, item_name)
					if os.path.isdir(source_path):
						conflict_path = None
						if os.path.exists(check_path_dir2):
							conflict_path = check_path_dir2
						elif os.path.exists(check_path_dir1):
							conflict_path = check_path_dir1
						if conflict_path:
							user_choice = QMessageBox.question(
								self,
								"Conflict Detected",
								f"The folder '{item_name}' already exists. Overwrite?",
								QMessageBox.Yes | QMessageBox.No
								)
							if user_choice == QMessageBox.Yes:
								shutil.rmtree(conflict_path)
							elif user_choice == QMessageBox.No:
								continue
						shutil.copytree(source_path, final_target_path, dirs_exist_ok=True)
				QMessageBox.information(self, "Success",
										f"All keyfile folders have been copied to deactivated directory.")
			except Exception as e:
				QMessageBox.critical(self, "Error", f"An error occurred: {e}")
		self.setup_table()
	
	def merge_database(self):
		r"""
		Import an external database. If conflicts occur, open a dialog and wait for manual resolution.
		"""
		merge_db, _ = QFileDialog.getOpenFileName(self,
								self.tr("Select Database to Import"),
								"",
								"Database Files (*.sqlite *.db)")
		if not merge_db:
			return
		db_handler_current = self.db_handler
		existing_data = db_handler_current.get_all_data_dict()
		db_handler_merge = DatabaseHandler(merge_db)
		try:
			db_handler_merge.connect()
			new_data = db_handler_merge.get_all_data_dict()
			db_handler_merge.close()
		except Exception as e:
			QMessageBox.warning(
				self,
				self.tr("Error"),
				self.tr("Failed to load databases: {error}").format(error=e)
			)
			return
		new_records = []
		conflict_records = []
		identical_records = []
		for serial_number, new_record in new_data.items():
			if serial_number in existing_data:
				existing_record = existing_data[serial_number]
				if existing_record == new_record:
					identical_records.append(new_record)
				else:
					# keyfile_conflict = existing_record[-1] != new_record[-1]
					conflict_records.append((existing_record, new_record))
			else:
				new_records.append(new_record)
		for record in new_records:
			self.db_handler.insert_data(record)
		if conflict_records:
			dialog = DatabaseMerger(self.db_handler, conflict_records, self)
			dialog.exec_()
		self.db_handler.connection.commit()
		self.setup_table()
	
	def connect_database(self):
		r"""
		Open a file dialog to select a database file, connect to the
		selected database, and save the database path to the config.json file.
		"""
		self.db_path, _ = QFileDialog.getOpenFileName(self, self.tr("Select Database File"), "",
													  "Database Files (*.sqlite *.db)")
		if not self.db_path:
			return
		try:
			self.db_handler = DatabaseHandler(self.db_path)
			self.db_handler.connect()
			self.config_manager.save_db_path(self.db_path)
			self.setup_table()
		except Exception as e:
			QMessageBox.warning(
				self,
				self.tr("Database Connection Failed"),
				self.tr("Failed to connect to the database: {error}").format(error=e)
			)
	
	def new_database_dialog(self):
		r"""
		Open a dialog for selecting directory and creating a new database.
		"""
		file_path, _ = QFileDialog.getSaveFileName(self,
												self.tr("Select Directory and Enter Database Name"),
												"",
												"SQLite Database files (*.db *.sqlite *.sqlite3)")
		if file_path:
			if not file_path.lower().endswith(('.db', '.sqlite', '.sqlite3', '.db3')):
				file_path += '.db'
			try:
				self.db_handler = DatabaseHandler(file_path)
				self.db_handler.connect()
				self.db_handler.create_table()
				self.db_handler.connection.commit()
				self.config_manager.db_path = file_path
				self.config_manager.save_db_path(file_path)
				self.setup_table()
				self.db_path = file_path
			except sqlite3.DatabaseError as e:
				QMessageBox.warning(
					self,
					self.tr("Database Creation Failed"),
					self.tr("Failed to create a new database: {error}").format(error=e)
				)
		else:
			pass
	
	def open_setting_dialog(self):
		r"""
		Open a dialog for selecting two directories and database file.
		If valid, initialize KeyHandler, FolderContent, and DatabaseHandler, and save the paths to the config.json file.
		"""
		dialog = QDialog(self)
		open_ui = Ui_Open()
		open_ui.setupUi(dialog)
		dialog.resize(800, 300)
		self.config_manager.open_ui = open_ui
		open_ui.acBrowseButton.clicked.connect(lambda: self.config_manager.select_directory1(dialog, open_ui))
		open_ui.deacBrowseButton.clicked.connect(lambda: self.config_manager.select_directory2(dialog, open_ui))
		open_ui.dbBrowseButton.clicked.connect(lambda: self.config_manager.select_db_path(dialog, open_ui))
		dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
		dialog.setWindowTitle(self.tr("Database & Directory Settings"))
		# Pre-fill the input fields if the directories have already been selected previously
		if self.directory1 and self.directory2 and self.db_path:
			open_ui.acLineEdit.setText(self.directory1)
			open_ui.deacLineEdit.setText(self.directory2)
			open_ui.dbLineEdit.setText(self.db_path)
		open_ui.confirmButton.clicked.connect(lambda: self.config_manager.confirm_directory_selection(dialog, open_ui))
		open_ui.cancelButton.clicked.connect(dialog.reject)
		if dialog.exec_():
			if self.config_manager.directory1 and self.config_manager.directory2:
				self.directory1 = self.config_manager.directory1
				self.directory2 = self.config_manager.directory2
				self.db_path = self.config_manager.db_path
				self.config_manager.save_config()
				self.initialize_handlers()
	
	def initialize_handlers(self):
		r"""
		Initialize KeyHandler, FolderContent and DatabaseHandler based on the selected directory paths and database file.
		If success, set up the table for further operations.
		"""
		self.key_handler = KeyHandler(self.directory1, self.directory2)
		if not self.key_handler.check_directories():
			QMessageBox.warning(self, "Error", self.tr("Directory validation failure"))
			return
		self.folder_content = FolderContent(self.directory1, self.directory2)
		self.db_handler = DatabaseHandler(self.db_path)
		self.db_handler.connect()
		self.setup_table()
	
	def quick_import_keyfile(self):
		r"""
		Quickly import new keyfiles into the database.
		This method identifies keyfiles which "not exists" in the database, retrieves their corresponding
		sensor names and serial numbers, and inserts them into the database with minimal information.
		"""
		serial_numbers = []
		for row in range(self.ui.tableWidget.rowCount()):
			key_item = self.ui.tableWidget.item(row, 10)
			db_status = key_item.data(Qt.UserRole)
			if db_status == DBStatus.NOT_EXISTS:
				serial_number = key_item.data(Qt.UserRole + 2)
				serial_numbers.append(serial_number)
		if not serial_numbers:
			QMessageBox.information(
				self,
				self.tr("Import"),
				self.tr("No new keyfiles found to import.")
			)
			return
		sensor_names = [self.folder_content.read_sensor_name_for_key(sn) for sn in serial_numbers]
		for serial_number, sensor_name in zip(serial_numbers, sensor_names):
			if sensor_name:
				row_data = [
					serial_number,
					sensor_name,
					None,
					None,
					None,
					None,
					None,
					None,
					None
				]
				self.db_handler.insert_data(row_data)
		self.db_handler.commit()
		self.update_table_row(serial_numbers)
	
	def rename_sensor_name(self):
		r"""
		Rename the sensor name both in the database and keyfile. Only work for the first selected entry.
		"""
		checked_serial_numbers = self.get_checked_serial_numbers()
		serial_numbers = [sn for sn in checked_serial_numbers if self.check_db_status(sn) != DBStatus.NOT_EXISTS]
		if not serial_numbers:
			return
		serial_number = serial_numbers[0]
		row = None
		for r in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.item(r, 2) and self.ui.tableWidget.item(r, 2).text() == serial_number:
				row = r
				break
		sensor_name = self.ui.tableWidget.item(row, 3).text()
		if sensor_name:
			dialog = RenameSensor(serial_number, sensor_name, parent=self)
			if dialog.exec_() == QDialog.Accepted:
				new_name = dialog.get_new_sensor_name()
				self.db_handler.update_name(serial_number, new_name)
				self.folder_content.edit_sensor_name_for_key(serial_number, new_name)
				logging.info(f"Sensor name updated for Serial Number {serial_number}: {sensor_name} -> {new_name}")
				self.update_table_row([serial_number])
		self.reset_all_checkboxes()
		self.db_handler.commit()
	
	def check_db_status(self, serial_number):
		r"""
		Check the database status for a given serial number.
		\param serial_number (str): The serial number to check.
		\return (DBStatus): The database status of the given serial number, or None if not found.
		"""
		for row in range(self.ui.tableWidget.rowCount()):
			key_item = self.ui.tableWidget.item(row, 10)
			if key_item and key_item.data(Qt.UserRole + 2) == serial_number:
				db_status = key_item.data(Qt.UserRole)
				return db_status
		return None
	
	def check_activation_status(self, serial_number):
		r"""
		Check the activation status for a given serial number.
		\param serial_number (str): The serial number to check.
		\return (ActivationStatus): The activation status of the given serial number, or None if not found.
		"""
		for row in range(self.ui.tableWidget.rowCount()):
			key_item = self.ui.tableWidget.item(row, 10)
			if key_item and key_item.data(Qt.UserRole + 2) == serial_number:
				activation_item = self.ui.tableWidget.item(row, 1)
				activation_status = activation_item.data(Qt.UserRole + 1)
				return activation_status
		return None
	
	def get_checked_serial_numbers(self):
		r"""Retrieve serial numbers for rows where the checkbox is checked.	"""
		serial_numbers = []
		for row in range(self.ui.tableWidget.rowCount()):
			checkbox_item = self.ui.tableWidget.item(row, 0)
			if checkbox_item and checkbox_item.checkState() == Qt.Checked:
				key_item = self.ui.tableWidget.item(row, 10)
				keyfile = key_item.data(Qt.UserRole + 2)
				serial_numbers.append(keyfile)
		return serial_numbers
	
	def reset_all_checkboxes(self):
		r"""Reset all checkboxes in the table to an unchecked state."""
		for row in range(self.ui.tableWidget.rowCount()):
			checkbox_item = self.ui.tableWidget.item(row, 0)
			if checkbox_item and checkbox_item.flags() & Qt.ItemIsUserCheckable:
				checkbox_item.setCheckState(Qt.Unchecked)
	
	def import_keyfile_to_db(self):
		r"""Import selected keyfiles to database with minimum content (serial number and sensor name only). """
		checked_serial_numbers = self.get_checked_serial_numbers()
		serial_numbers = [sn for sn in checked_serial_numbers if self.check_db_status(sn) == DBStatus.NOT_EXISTS]
		if not serial_numbers:
			return
		sensor_names = [self.folder_content.read_sensor_name_for_key(sn) for sn in serial_numbers]
		for serial_number, sensor_name in zip(serial_numbers, sensor_names):
			if sensor_name:
				row_data = [
					serial_number,
					sensor_name,
					None,
					None,
					None,
					None,
					None,
					None,
					None
				]
				self.db_handler.insert_data(row_data)
		self.db_handler.commit()
		self.reset_all_checkboxes()
		self.update_table_row(serial_numbers)
	
	def upload_changes_db(self):
		r"""
		Save all changes in the table (add, modify, delete rows) to the database.
		Logs each action (insertion, deletion, update) with log file.
		"""
		if self.db_handler is None:
			return
		try:
			db_data = self.db_handler.get_all_data_dict()
			table_data = {}
			row_count = self.ui.tableWidget.rowCount()
			column_count = self.ui.tableWidget.columnCount()
			for row in range(row_count):
				row_data = []
				for col in range(2, column_count - 2):
					item = self.ui.tableWidget.item(row, col)
					if item is not None:
						text = item.text()
						row_data.append(text if text != '' else None)
					else:
						row_data.append(None)
				serial_number = row_data[0]
				if serial_number is not None:
					table_data[serial_number] = row_data
				else:
					for col in range(2, column_count - 2):
						self.ui.tableWidget.setItem(row, col, QTableWidgetItem(""))
			db_serial_numbers = set(db_data.keys())
			table_serial_numbers = set(table_data.keys())
			serials_to_add = table_serial_numbers - db_serial_numbers
			serials_to_delete = db_serial_numbers - table_serial_numbers
			serials_possible_update = db_serial_numbers & table_serial_numbers
			updated_serials = []
			for serial in serials_to_delete:
				self.db_handler.delete_data(serial)
				logging.info(f"Deleted data for serial number: {serial}")
			for serial in serials_to_add:
				row_data = table_data[serial]
				row_data.append(None)
				self.db_handler.insert_data(row_data)
				logging.info(f"Inserted new data for serial number: {serial}, data: {row_data}")
				updated_serials.append(serial)
			for serial in serials_possible_update:
				db_row = db_data[serial]
				table_row = table_data[serial]
				if db_row[:-1] != tuple(table_row):
					self.db_handler.update_data(table_row)
					logging.info(
						f"Updated data for serial number: {serial}, old data: {db_row[:-1]}, new data: {table_row}")
					updated_serials.append(serial)
			self.db_handler.connection.commit()
			# Refresh only updated rows
			self.update_table_row(updated_serials)
		except Exception as e:
			QMessageBox.warning(
				self,
				self.tr("Error"),
				self.tr("Error saving changes: {error}").format(error=e)
			)
	
	def attach_keyfile_to_db(self):
		r"""
		Zip the folder and attach a keyfile to an existing database record that is missing a keyfile.
		After attaching, the table is refreshed, and the operation is logged.
		"""
		try:
			checked_serial_numbers = self.get_checked_serial_numbers()
			serial_numbers = [
				sn for sn in checked_serial_numbers
				if self.check_db_status(sn) == DBStatus.MISSING_KEYFILE and self.check_activation_status(sn) != ActivationStatus.UNKNOWN
			]
			if not serial_numbers:
				return
			for serial_number in serial_numbers:
				activation_status = self.check_activation_status(serial_number)
				status = "activated" if activation_status == ActivationStatus.ACTIVATED else "deactivated"
				folder_path = self.key_handler.key_folder_path(serial_number, status)
				zip_buffer = self.db_handler.create_zip_from_folder(folder_path)
				self.db_handler.update_blob_data(zip_buffer.getvalue(), serial_number)
				logging.info(f"Keyfile for serial number '{serial_number}' successfully attached.")
			self.db_handler.commit()
			self.reset_all_checkboxes()
			self.update_table_row(serial_numbers)
		except Exception as e:
			self.db_handler.rollback()
			QMessageBox.warning(
				self,
				self.tr("Error"),
				self.tr(f"An error occurred while attaching keyfiles: {e}")
			)
			logging.error(f"Error occurred while attaching keyfiles: {e}")
	
	def replace_keyfile_db_disk(self):
		r"""Replace the keyfile between the database and disk when there is a mismatch."""
		try:
			checked_serial_numbers = self.get_checked_serial_numbers()
			serial_numbers = [
				sn for sn in checked_serial_numbers
				if self.check_db_status(sn) == DBStatus.MISMATCH and self.check_activation_status(sn) != ActivationStatus.UNKNOWN
			]
			if not serial_numbers:
				return
			path_list = []
			for serial_number in serial_numbers:
				activation_status = self.check_activation_status(serial_number)
				status = "activated" if activation_status == ActivationStatus.ACTIVATED else "deactivated"
				folder_path = self.key_handler.key_folder_path(serial_number, status)
				path_list.append(folder_path)
			dialog = KeyfileReplace(serial_numbers, self.db_handler, path_list, is_batch_mode=len(serial_numbers) > 1,
									parent=self)
			dialog.exec_()
			self.reset_all_checkboxes()
			self.update_table_row(serial_numbers)
		except Exception as e:
			logging.error(f"Error occurred during keyfile replacement: {e}")
			QMessageBox.warning(
				self,
				self.tr("Error"),
				self.tr(f"An error occurred during keyfile replacement: {e}")
			)
	
	def copy_keyfile_to_disk(self):
		r"""Copy keyfile from the database to disk, for keyfiles that only exist in the database but not on disk."""
		checked_serial_numbers = self.get_checked_serial_numbers()
		serial_numbers = [
			sn for sn in checked_serial_numbers
			if self.check_db_status(sn) == DBStatus.EXISTS and self.check_activation_status(sn) == ActivationStatus.UNKNOWN
		]
		if not serial_numbers:
			return
		for serial_number in serial_numbers:
			output_folder_path = os.path.join(self.directory1, serial_number)
			# reply = QMessageBox.question(
			# 	self,
			# 	self.tr("Confirm Copy"),
			# 	self.tr("Are you sure you want to copy the file '{serial_number}' to disk?").format(
			# 		serial_number=serial_number),
			# 	QMessageBox.Yes | QMessageBox.No,
			# 	QMessageBox.No
			# )
			#
			# if reply == QMessageBox.Yes:
			try:
				self.db_handler.fetch_blob_and_save_as_folder(serial_number, output_folder_path)
				self.db_handler.commit()
				self.update_table_row([serial_number])
				logging.info(
					f"The file {serial_number} was successfully copied to the disk path {output_folder_path}.")
			except Exception as e:
				QMessageBox.warning(
					self,
					self.tr("Error"),
					self.tr("Copy file failed: {error}").format(error=str(e))
				)
				logging.error(f"Error copying file {serial_number} to disk: {str(e)}")
	
	def update_db_attached_keyfile(self):
		r"""
		Manually select a folder from any location, zip it, and attach it to an existing database record.
		This will overwrite the original keyfile stored in the database.
		After attaching, the table is refreshed, and the operation is logged.
		"""
		try:
			checked_serial_numbers = self.get_checked_serial_numbers()
			serial_numbers = [
				sn for sn in checked_serial_numbers
				if self.check_db_status(sn) == DBStatus.EXISTS or DBStatus.MISMATCH
			]
			if not serial_numbers:
				return
			serial_number = serial_numbers[0]
			folder_path = QFileDialog.getExistingDirectory(
				self,
				self.tr("Please select the folder to attach"),
				""
			)
			if not folder_path:
				return
			zip_buffer = self.db_handler.create_zip_from_folder(folder_path)
			# reply = QMessageBox.question(self, self.tr("Confirm Attach"),
			# 							 self.tr("Are you sure you want to attach the keyfile into the database?"),
			# 							 QMessageBox.Yes | QMessageBox.No)
			#
			# if reply == QMessageBox.No:
			# 	return
			self.db_handler.update_blob_data(zip_buffer.getvalue(), serial_number)
			self.db_handler.commit()
			logging.info(
				f"The Keyfile '{os.path.basename(folder_path)}' was successfully zipped and attached to the database.")
			# QMessageBox.information(
			# 	self,
			# 	self.tr("Success"),
			# 	self.tr(f"Keyfile '{os.path.basename(folder_path)}' has been successfully attached to the database.")
			# )
			self.reset_all_checkboxes()
			self.update_table_row([serial_number])
		except Exception as e:
			self.db_handler.rollback()
			QMessageBox.warning(
				self,
				self.tr("Error"),
				self.tr("Error occurred while attaching the keyfile: {error}").format(error=e)
			)
			logging.error(f"Error occurred while attaching the keyfile:{e}")
	
	def open_filter_widget(self):
		r"""Control visibility of filter widget"""
		self.ui.filterDockWidget.setVisible(not self.ui.filterDockWidget.isVisible())

	def open_info_widget(self):
		r"""Control visibility of extra information widget"""
		self.ui.infoDockWidget.setVisible(not self.ui.infoDockWidget.isVisible())

	def open_search_widget(self):
		r"""Control visibility of full text search widget"""
		self.ui.searchDockWidget.setVisible(not self.ui.searchDockWidget.isVisible())

	def table_cell_info(self, row, column):
		r"""
		Display relevant information on the right side panel for the selected table cell.
		\param row (int): The row index of the selected table cell.
		\param column (int): The column index of the selected table cell.
		"""
		if column == 0 or column == 1:
			return
		key_item = self.ui.tableWidget.item(row, 10)
		if key_item is None or key_item.data(Qt.UserRole + 2) is None:
			return
		key = key_item.data(Qt.UserRole + 2)
		user_properties = self.folder_content.read_user_properties(key)
		gage_segment = self.folder_content.read_gage_segment(key)
		od6ref_file = self.folder_content.read_od6ref_file(key)
		output = ""
		if user_properties is not None:
			output += "<h3>user_properties.json</h3>"
			formatted_json = json.dumps(user_properties, indent=4, ensure_ascii=False)
			output += format_json_to_html(formatted_json)
		else:
			output += " "
		if gage_segment is not None:
			output += "<h3>gage_segment.json</h3>"
			formatted_json = json.dumps(gage_segment, indent=4, ensure_ascii=False)
			output += format_json_to_html(formatted_json)
		else:
			output += " "
		if od6ref_file is not None:
			output += "<h3>.od6ref</h3>"
			formatted_json = json.dumps(od6ref_file, indent=4, ensure_ascii=False)
			output += format_json_to_html(formatted_json)
		else:
			output += " "
		self.ui.infoTextBrowser.setHtml(output)
	
	def setup_table(self):
		r"""
		Set up the table with the necessary headers, styles, and configurations.
		Enables the ability to drag and move columns for custom arrangement.
		Sets certain columns (Status, Serial Number, and Keyfile) as read-only to prevent unintended modification.
		Populate table with data in database, and connect a cell click event to display additional information.
		"""
		self.ui.tableWidget.setColumnCount(12)
		self.ui.tableWidget.setHorizontalHeaderLabels([
			' ',
			self.tr('Status'),
			self.tr('Serial Number'),
			self.tr('Sensor Name'),
			self.tr('Project'),
			self.tr('Operator'),
			self.tr('Specimen'),
			self.tr('DFOS_Type'),
			self.tr('Installation'),
			self.tr('Note'),
			self.tr('Keyfile'),
			self.tr('Last Edit Date')
		])
		self.ui.tableWidget.setStyleSheet("""
			QHeaderView::section {
				background-color: lightgray;
				color: black;
				font-weight: bold;
				height: 30px; 
				border: 1px solid black;
			}
			QTableWidget {
				gridline-color: grey;
			}
			# QTableWidget::item:selected {
			# 	background-color: transparent;
			# 	color: black; 
			# }
		""")
		self.ui.tableWidget.setColumnWidth(0, 10)
		self.ui.tableWidget.setColumnWidth(1, 180)
		header = self.ui.tableWidget.horizontalHeader()
		header.setSectionsMovable(True)
		header.setDragEnabled(True)
		header.setDragDropMode(QHeaderView.DragDrop)
		header.moveSection(header.visualIndex(2), 9)
		if self.key_handler is None:
			return
		self.ui.tableWidget.setRowCount(0)
		self.populate_table()
		self.set_columns_read_only([1, 2, 3, 10, 11])
		self.set_columns_background_color([2, 3, 10, 11])
		self.populate_search_combobox()
	
	def set_columns_read_only(self, columns):
		r"""
		Set the specified columns to read-only.
		These columns will still allow user interaction like selection and clicking, but their content will not be editable
		\param columns (List[int]): A list of column indices that should be set to read-only.
		"""
		row_count = self.ui.tableWidget.rowCount()
		for row in range(row_count):
			for column in columns:
				item = self.ui.tableWidget.item(row, column)
				if item:
					item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
	
	def set_columns_background_color(self, columns):
		r"""
		Apply a light gray background color to the specified columns.
		\param columns (List[int]): A list of column indices (integers) to apply the background color.
		"""
		row_count = self.ui.tableWidget.rowCount()
		for row in range(row_count):
			for column in columns:
				item = self.ui.tableWidget.item(row, column)
				if item:
					item.setBackground(QBrush(QColor(245, 245, 245)))
	
	def populate_table(self):
		r"""
		Populate the table with key data and statuses from disk and database.
		Retrieve key information from the disk and the database, checking for activation deactivation status,
		existence in the database, and possible mismatches between the keyfile in disk and in the database.
		"""
		# start_time = time.time()
		self.ui.tableWidget.setSortingEnabled(False)
		activated_keys = set(self.key_handler.read_keys('activated'))
		deactivated_keys = set(self.key_handler.read_keys('deactivated'))
		database_keys = set(self.db_handler.read_keys())
		keys_with_status = []
		all_keys = activated_keys | deactivated_keys
		db_only_keys = database_keys - all_keys
		activated_only_keys = activated_keys - database_keys
		deactivated_only_keys = deactivated_keys - database_keys
		for key in database_keys & all_keys:
			blob_data = self.db_handler.get_blob_data(key)
			path = None
			status = None
			mismatch = False
			if key in activated_keys:
				path = os.path.join(self.directory1, key)
				status = 'Activated'
			elif key in deactivated_keys:
				path = os.path.join(self.directory2, key)
				status = 'Deactivated'
			if blob_data and path and os.path.exists(path) and os.path.isdir(path):
				with tempfile.TemporaryDirectory() as temp_dir:
					try:
						with zipfile.ZipFile(io.BytesIO(blob_data), 'r') as zip_ref:
							zip_ref.extractall(temp_dir)
						temp_hashes = self.get_folder_hashes(temp_dir)
						local_hashes = self.get_folder_hashes(path)
						if temp_hashes != local_hashes:
							mismatch = True
					except Exception as e:
						print(f"An error occurred during comparison: {e}")
						mismatch = True
			keys_with_status.append((key, status, mismatch))
		keys_with_status += [(key, 'Activated', False) for key in activated_only_keys]
		keys_with_status += [(key, 'Deactivated', False) for key in deactivated_only_keys]
		keys_with_status += [(key, 'Database Only', False) for key in db_only_keys]
		self.ui.tableWidget.setRowCount(len(keys_with_status))
		for index, (key, status, mismatch) in enumerate(keys_with_status):
			for col in range(12):
				if self.ui.tableWidget.item(index, col) is None:
					self.ui.tableWidget.setItem(index, col, QTableWidgetItem())
			mismatch_keyfile_icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
			if status == 'Activated':
				activation_status = ActivationStatus.ACTIVATED
				self.ui.tableWidget.setCellWidget(index, 1, self.create_status_button('Activated'))
			elif status == 'Deactivated':
				activation_status = ActivationStatus.DEACTIVATED
				self.ui.tableWidget.setCellWidget(index, 1, self.create_status_button('Deactivated'))
			else:
				activation_status = ActivationStatus.UNKNOWN
				self.ui.tableWidget.setCellWidget(index, 1, self.create_status_button('Unknown'))
			activation_item = self.ui.tableWidget.item(index, 1)
			activation_item.setData(Qt.DisplayRole, activation_status.value)
			activation_item.setForeground(Qt.transparent)
			activation_item.setData(Qt.UserRole + 1, activation_status)
			check_item = self.ui.tableWidget.item(index, 0)
			check_item.setCheckState(Qt.Unchecked)
			if self.db_handler.key_exists_in_database(key):
				details = list(self.db_handler.get_key_details(key))
				if not status == "Database Only":
					details[8] = key
			else:
				details = ("", "", "", "", "", "", "", "", key)
			self.ui.tableWidget.item(index, 2).setText(details[0])
			self.ui.tableWidget.item(index, 3).setText(details[1])
			self.ui.tableWidget.item(index, 4).setText(details[2])
			self.ui.tableWidget.item(index, 5).setText(details[3])
			self.ui.tableWidget.item(index, 6).setText(details[4])
			self.ui.tableWidget.item(index, 7).setText(details[5])
			self.ui.tableWidget.item(index, 8).setText(details[6])
			self.ui.tableWidget.item(index, 9).setText(details[7])
			if isinstance(details[8], str):
				keyfile_text = details[8]
			elif isinstance(details[8], bytes):
				keyfile_text = details[0]
			else:
				keyfile_text = ""
			folder_on_icon = QIcon(resource_path('resources/icons/folder_on.svg'))  # Folder exists
			folder_off_icon = QIcon(resource_path('resources/icons/folder_off.svg'))  # Folder missing
			db_on_icon = QIcon(resource_path('resources/icons/db_on.svg'))  # Database exists
			db_off_icon = QIcon(resource_path('resources/icons/db_off.svg'))  # Database missing
			key_item = self.ui.tableWidget.item(index, 10)
			key_item.setData(Qt.UserRole + 2, keyfile_text)
			if status == 'Activated' or status == 'Deactivated':
				if self.db_handler.key_exists_in_database(key) and self.db_handler.key_exists_in_keyfile(key):
					icons = [folder_on_icon, db_on_icon]
					widget = create_keyfile_cell_widget(icons, keyfile_text)
					key_item.setData(Qt.UserRole, DBStatus.EXISTS)
					if mismatch:
						icons.append(mismatch_keyfile_icon)
						widget = create_keyfile_cell_widget(icons, keyfile_text)
						key_item.setData(Qt.UserRole, DBStatus.MISMATCH)
				elif self.db_handler.key_exists_in_database(key) and not self.db_handler.key_exists_in_keyfile(key):
					icons = [folder_on_icon, db_off_icon]
					widget = create_keyfile_cell_widget(icons, keyfile_text)
					key_item.setData(Qt.UserRole, DBStatus.MISSING_KEYFILE)
				else:
					icons = [folder_on_icon, db_off_icon]
					widget = create_keyfile_cell_widget(icons, keyfile_text)
					key_item.setData(Qt.UserRole, DBStatus.NOT_EXISTS)
			else:
				if self.db_handler.key_exists_in_database(key) and self.db_handler.key_exists_in_keyfile(key):
					icons = [folder_off_icon, db_on_icon]
					widget = create_keyfile_cell_widget(icons, keyfile_text)
					key_item.setData(Qt.UserRole, DBStatus.EXISTS)
				else:
					icons = [folder_off_icon, db_off_icon]
					widget = create_keyfile_cell_widget(icons, keyfile_text)
					key_item.setData(Qt.UserRole, DBStatus.MISSING_KEYFILE)
			self.ui.tableWidget.setCellWidget(index, 10, widget)
			edit_date = self.folder_content.get_last_edit_date(key)
			edit_date_str = edit_date.strftime("%Y-%m-%d") if edit_date else ""
			self.ui.tableWidget.item(index, 11).setText(edit_date_str)
		self.ui.tableWidget.setSortingEnabled(True)
		# end_time = time.time()
		# print(f"Time taken to populate table: {end_time - start_time:.2f} seconds")
	
	def get_folder_hashes(self, folder_path):
		r"""
		Get hash values of all files in the folder.
		\param folder_path (str): The path to the folder.
		\return (dict): A dictionary with relative file paths as keys and hash values as values.
		"""
		file_hashes = {}
		for root, dirs, files in os.walk(folder_path):
			for file in sorted(files):
				file_path = os.path.join(root, file)
				relative_path = os.path.relpath(file_path, start=folder_path)
				with open(file_path, 'rb') as f:
					file_content = f.read()
				file_hash = hashlib.md5(file_content).hexdigest()
				file_hashes[relative_path] = file_hash
		return file_hashes
	
	def create_status_button(self, status):
		r"""
		Creates a colored QPushButton based on its activation status.
		The button will be colored differently depending on whether the status is 'Activated',
		'Deactivated', or 'Unknown'. The button is not clickable and will display the status text.
		\param status (str): The activation status ('Activated', 'Deactivated', 'Unknown').
		\return (QWidget): A QWidget containing the styled QPushButton for status display.
		"""
		status_translation_map = {
			'Activated': self.tr("Activated"),
			'Deactivated': self.tr("Deactivated"),
			'Unknown': self.tr("Unknown")
		}
		translated_status = status_translation_map[status]
		button = QPushButton(translated_status)
		button.setFixedSize(QSize(120, 20))
		button.setEnabled(False)
		# green
		if status == 'Activated':
			button.setStyleSheet("""
				background-color: #228B22;
				color: white;
				border-radius: 10px;
				font-weight: bold;
			""")
		# grey
		elif status == 'Deactivated':
			button.setStyleSheet("""
				background-color: #D3D3D3;
				color: black;
				border-radius: 10px;
				font-weight: bold;
			""")
		# yellow
		else:
			button.setStyleSheet("""
				background-color: #FFD700;
				color: black;
				border-radius: 10px;
				font-weight: bold;
			""")

		container = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(button)
		layout.setAlignment(Qt.AlignCenter)
		layout.setContentsMargins(0, 0, 0, 0)
		container.setLayout(layout)
		return container
	
	def toggle_activation(self):
		r"""
		Activate the selected items (checkbox is checked) in the table.
		If the activation status is 'Unknown', the checkbox is cleared and the row is skipped (because there is no such
		keyfile in disk to operate). For valid items, the keyfile moved from deactivated directory to activate directory.
		Upon successful activation, the item's status is updated to 'Activated' and the status button is turn green.
		"""
		for i in range(self.ui.tableWidget.rowCount()):
			check_item = self.ui.tableWidget.item(i, 0)
			activation_item = self.ui.tableWidget.item(i, 1)
			key_file = self.ui.tableWidget.item(i, 10).data(Qt.UserRole + 2)
			activation_status = activation_item.data(Qt.UserRole + 1)
			if activation_status == ActivationStatus.UNKNOWN:
				check_item.setCheckState(Qt.Unchecked)
				continue
			if check_item.checkState() == Qt.Checked:
				success = self.key_handler.activate_key(key_file)
				if success:
					activation_item.setData(Qt.UserRole + 1, ActivationStatus.ACTIVATED)
					self.ui.tableWidget.setCellWidget(i, 1, self.create_status_button('Activated'))
				check_item.setCheckState(Qt.Unchecked)
	
	def toggle_deactivation(self):
		r"""
		Deactivate the selected item (checkbox is checked) in the table.
		If the activation status is 'Unknown', the checkbox is cleared and the row is skipped (because there is no such
		keyfile in disk to operate). For valid items, the keyfile moved from the activated directory to the deactivated directory.
		Upon successful deactivation, the item's status is updated to 'Deactivated', and the status button turns grey.
		"""
		for i in range(self.ui.tableWidget.rowCount()):
			check_item = self.ui.tableWidget.item(i, 0)
			activation_item = self.ui.tableWidget.item(i, 1)
			key_file = self.ui.tableWidget.item(i, 10).data(Qt.UserRole + 2)
			activation_status = activation_item.data(Qt.UserRole + 1)
			if activation_status == ActivationStatus.UNKNOWN:
				check_item.setCheckState(Qt.Unchecked)
				continue
			if check_item.checkState() == Qt.Checked:
				success = self.key_handler.deactivate_key(key_file)
				if success:
					activation_item.setData(Qt.UserRole + 1, ActivationStatus.DEACTIVATED)
					self.ui.tableWidget.setCellWidget(i, 1, self.create_status_button('Deactivated'))
				check_item.setCheckState(Qt.Unchecked)
	
	def switch_language(self, language):
		r"""
		Switch the UI language and save it to the configuration file.
		\param language (str): The target language, either 'English' or 'German'.
		"""
		if language == 'german':
			# self.translator.load(os.path.join(os.path.dirname(__file__), '../resources/translations/Translate_DE.qm'))
			translation_path = resource_path('resources/translations/Translate_DE.qm')
			self.translator.load(translation_path)
			QApplication.instance().installTranslator(self.translator)
		elif language == 'english':
			QApplication.instance().removeTranslator(self.translator)
		self.populate_search_combobox()
		self.ui.retranslateUi(self)
		self.config_manager.language = language
		self.config_manager.save_config()
		self.setup_table()
	
	def exit_application(self):
		r"""Method to handle application exit."""
		QCoreApplication.instance().quit()
	
	def open_documentation(self):
		r"""Open the Doxygen generated documentation web page."""
		documentation_url = "https://tud-imb.github.io/fosKeyMan/"
		webbrowser.open(documentation_url)
	
	def populate_search_combobox(self):
		r"""
		Populate QComboBox with the keyfiles.
		"""
		self.ui.searchComboBox.clear()
		self.ui.searchComboBox.addItem(self.tr("Search Selected"))
		keyfiles = set()
		for row in range(self.ui.tableWidget.rowCount()):
			item = self.ui.tableWidget.item(row, 10)
			if item:
				keyfile = item.data(Qt.UserRole + 2)
				if keyfile:
					keyfiles.add(keyfile)
		for key in sorted(keyfiles):
			self.ui.searchComboBox.addItem(key)

	def execute_search(self):
		r"""
		Perform search based on the selected key item in the comboBox and display the results in TextBrowser.
		"""
		key = self.ui.searchComboBox.currentText()
		if key == self.tr("Search Selected"):
			key = None
		search_term = self.ui.searchLineEdit.text()
		if not search_term:
			self.ui.searchTextBrowser.setPlainText(self.tr("Search term cannot be empty. Please enter a search term."))
			return
		search_results = self.folder_content.full_text_search(search_term, key)
		self.ui.searchTextBrowser.clear()
		if search_results:
			# self.ui.searchTextBrowser.append("Search Results:\n")
			for key, match in search_results:
				result_text = f"Keyfile: {key}.zip\n"
				for entry in match:
					result_text += "\n".join([f"{k}: {v}" for k, v in entry.items()]) + "\n"
				result_text += "\n\n"
				self.ui.searchTextBrowser.append(result_text)
		else:
			self.ui.searchTextBrowser.setPlainText(self.tr("No results found."))
	
	def update_table_row(self, serial_numbers):
		r"""
		Update specific rows in the table given a list of serial numbers.
		\param serial_numbers (List[str]): A list of serial numbers for the rows to be updated.
		"""
		for serial_number in serial_numbers:
			row_index = None
			for row in range(self.ui.tableWidget.rowCount()):
				key_item = self.ui.tableWidget.item(row, 10)
				if key_item and key_item.data(Qt.UserRole + 2) == serial_number:
					row_index = row
					break
			if row_index is None:
				print(f"Serial number {serial_number} not found in the table.")
				continue
			status = None
			mismatch = False
			blob_data = self.db_handler.get_blob_data(serial_number)
			path = None
			if serial_number in self.key_handler.read_keys('activated'):
				status = 'Activated'
				path = os.path.join(self.directory1, serial_number)
			elif serial_number in self.key_handler.read_keys('deactivated'):
				status = 'Deactivated'
				path = os.path.join(self.directory2, serial_number)
			else:
				status = 'Unknown'
			if blob_data and path and os.path.exists(path) and os.path.isdir(path):
				with tempfile.TemporaryDirectory() as temp_dir:
					try:
						with zipfile.ZipFile(io.BytesIO(blob_data), 'r') as zip_ref:
							zip_ref.extractall(temp_dir)
						temp_hashes = self.get_folder_hashes(temp_dir)
						local_hashes = self.get_folder_hashes(path)
						if temp_hashes != local_hashes:
							mismatch = True
					except Exception as e:
						print(f"An error occurred during comparison: {e}")
						mismatch = True
			for col in range(12):
				if self.ui.tableWidget.item(row_index, col) is None:
					self.ui.tableWidget.setItem(row_index, col, QTableWidgetItem())
			if status == 'Activated':
				activation_status = ActivationStatus.ACTIVATED
				self.ui.tableWidget.setCellWidget(row_index, 1, self.create_status_button('Activated'))
			elif status == 'Deactivated':
				activation_status = ActivationStatus.DEACTIVATED
				self.ui.tableWidget.setCellWidget(row_index, 1, self.create_status_button('Deactivated'))
			else:
				activation_status = ActivationStatus.UNKNOWN
				self.ui.tableWidget.setCellWidget(row_index, 1, self.create_status_button('Unknown'))
			activation_item = self.ui.tableWidget.item(row_index, 1)
			activation_item.setData(Qt.UserRole + 1, activation_status)
			check_item = self.ui.tableWidget.item(row_index, 0)
			check_item.setCheckState(Qt.Unchecked)
			if self.db_handler.key_exists_in_database(serial_number):
				details = list(self.db_handler.get_key_details(serial_number))
				if not status == "Database Only":
					details[8] = serial_number
			else:
				details = ("", "", "", "", "", "", "", "", serial_number)
			self.ui.tableWidget.item(row_index, 2).setText(details[0])
			self.ui.tableWidget.item(row_index, 3).setText(details[1])
			self.ui.tableWidget.item(row_index, 4).setText(details[2])
			self.ui.tableWidget.item(row_index, 5).setText(details[3])
			self.ui.tableWidget.item(row_index, 6).setText(details[4])
			self.ui.tableWidget.item(row_index, 7).setText(details[5])
			self.ui.tableWidget.item(row_index, 8).setText(details[6])
			self.ui.tableWidget.item(row_index, 9).setText(details[7])
			key_item = self.ui.tableWidget.item(row_index, 10)
			key_item.setData(Qt.UserRole + 2, details[8])
			folder_on_icon = QIcon(resource_path('resources/icons/folder_on.svg'))
			folder_off_icon = QIcon(resource_path('resources/icons/folder_off.svg'))
			db_on_icon = QIcon(resource_path('resources/icons/db_on.svg'))
			db_off_icon = QIcon(resource_path('resources/icons/db_off.svg'))
			mismatch_keyfile_icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
			if status in ['Activated', 'Deactivated']:
				if self.db_handler.key_exists_in_database(serial_number) and self.db_handler.key_exists_in_keyfile(
						serial_number):
					icons = [folder_on_icon, db_on_icon]
					widget = create_keyfile_cell_widget(icons, details[8])
					key_item.setData(Qt.UserRole, DBStatus.EXISTS)
					if mismatch:
						icons.append(mismatch_keyfile_icon)
						widget = create_keyfile_cell_widget(icons, details[8])
						key_item.setData(Qt.UserRole, DBStatus.MISMATCH)
				else:
					icons = [folder_on_icon, db_off_icon]
					widget = create_keyfile_cell_widget(icons, details[8])
					key_item.setData(Qt.UserRole, DBStatus.MISSING_KEYFILE)
			else:
				icons = [folder_off_icon, db_off_icon]
				widget = create_keyfile_cell_widget(icons, details[8])
				key_item.setData(Qt.UserRole, DBStatus.MISSING_KEYFILE)
			self.ui.tableWidget.setCellWidget(row_index, 10, widget)
			edit_date = self.folder_content.get_last_edit_date(serial_number)
			edit_date_str = edit_date.strftime("%Y-%m-%d") if edit_date else ""
			self.ui.tableWidget.item(row_index, 11).setText(edit_date_str)


def file_path(relative_path):
	r"""
	Join the base directory with the given relative path to generate an absolute path.
	This function determines the base directory based on whether the application is running
	in a frozen state (e.g., when packaged with PyInstaller) or in a regular environment.
	\param relative_path (str): The relative path to the target file or directory.
	\return (str): The absolute path to the target file or directory.
	"""
	if getattr(sys, 'frozen', False):
		base_dir = os.path.dirname(sys.executable)
	else:
		base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_dir, relative_path)


def resource_path(relative_path):
	r"""
	Similar to file_path, it generates the absolute path to a resource.
	If the application is frozen (e.g., packaged with PyInstaller), it uses the _MEIPASS directory.
	\param relative_path (str): The relative path to the resource.
	\return (str): The absolute path to the resource.
	"""
	if getattr(sys, 'frozen', False):
		base_dir = sys._MEIPASS
	else:
		base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_dir, relative_path)


def create_keyfile_cell_widget(icons, text):
	r"""
	Creates a widget that displays a set of icons alongside a text label.
	(e.g., folder and database icons in front of a keyfile name).
	\param icons (list[QIcon]): A list of QIcon objects to be displayed.
	\param text (str): The text to display next to the icons.
	\return (QWidget): A QWidget containing the icons and the text label.
	"""
	widget = QWidget()
	layout = QHBoxLayout(widget)
	layout.setContentsMargins(0, 0, 0, 0)
	for icon in icons:
		label = QLabel()
		label.setPixmap(icon.pixmap(20, 20))
		layout.addWidget(label)
	text_label = QLabel(text)
	layout.addWidget(text_label)
	layout.addStretch()
	return widget


def main():
	r"""Initialize and run the application."""
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show_and_check_config()
	sys.exit(app.exec_())

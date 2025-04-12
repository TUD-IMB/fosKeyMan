
r"""
Defines the main Graphical User Interface.

\author Xiali Song, Bertram Richter
\date 2025
"""

import logging
import shutil
import sys
import os
import json
import webbrowser

from PySide6.QtGui import QIcon, QColor, QBrush
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QDialog, \
	QFileDialog, QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QComboBox, QDateEdit
from PySide6.QtCore import QTranslator, Qt, QCoreApplication, QSize, QDate

from frontend.columnconfigurator import ColumnConfigurator
from frontend.metadataeditor import MetadataEditor
from frontend.renamesensor import RenameSensor
from frontend.ui.uimain import Ui_MainWindow
from backend.keyhandler import KeyHandler
from backend.foldercontent import FolderContent
from frontend.configmanager import ConfigManager
from frontend.hoverinfo import HoverInfo
from frontend.tableoperator import TableOperator
from frontend.keystatus import ActivationStatus
from frontend.ui.uiopen import Ui_Open
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

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.directory1 = None
		self.directory2 = None
		self.key_handler = None
		self.folder_content = None
		self.config_manager = ConfigManager(file_path('fosKeyManConfig.json'))
		self.directory1, self.directory2, self.language, self.custom_columns = self.config_manager.check_and_load_previous_config()
		self.translator = QTranslator(self)
		self.table_operator = TableOperator(self.ui.tableWidget)
		self.connect_actions()
		self.hover_info = HoverInfo(self.ui.tableWidget, self)
		self.ui.tableWidget.cellClicked.connect(self.table_cell_info)
		self.ui.searchPushButton.clicked.connect(self.execute_search)
		self.setWindowIcon(QIcon(resource_path('resources/foskeyman_logo_short.svg')))
		self.adjust_window_size()
		self.dynamic_filter_inputs = {}

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
		
		If all required paths (directory1, directory2) are valid, it will set up the table.
		If any of the paths are missing, it will open the setting dialog for the user to initialize the configuration.
		"""
		self.show()
		self.switch_language(self.language)
		if self.directory1 and self.directory2:
			self.initialize_handlers()
			self.setup_table()
			self.setup_filter_dockwidget()
		else:
			self.open_setting_dialog()

	def setup_filter_dockwidget(self):
		layout = self.ui.filterFormLayout

		while layout.rowCount():
			layout.removeRow(0)

		self.dynamic_filter_inputs = {}

		status_label = QLabel("Status", self)
		status_combo = QComboBox(self)
		status_combo.addItems(["All", "Activated", "Deactivated"])
		layout.addRow(status_label, status_combo)
		self.dynamic_filter_inputs["Status"] = status_combo

		serial_label = QLabel("Serial Number", self)
		serial_input = QLineEdit(self)
		layout.addRow(serial_label, serial_input)
		self.dynamic_filter_inputs["Serial Number"] = serial_input

		name_label = QLabel("Sensor Name", self)
		name_input = QLineEdit(self)
		layout.addRow(name_label, name_input)
		self.dynamic_filter_inputs["Sensor Name"] = name_input

		for col in self.custom_columns:
			label = QLabel(col, self)
			line_edit = QLineEdit(self)
			line_edit.setObjectName(f"{col.lower().replace(' ', '')}LineEdit")
			layout.addRow(label, line_edit)
			self.dynamic_filter_inputs[col] = line_edit

		date_container = QWidget(self)
		date_layout = QHBoxLayout(date_container)
		date_layout.setContentsMargins(0, 0, 0, 0)

		start_label = QLabel("Start", self)
		start_date_edit = QDateEdit(self)
		start_date_edit.setDisplayFormat("yyyy-MM-dd")
		start_date_edit.setCalendarPopup(True)
		start_date_edit.setDate(QDate(2000, 1, 1))

		end_label = QLabel("End", self)
		end_date_edit = QDateEdit(self)
		end_date_edit.setDisplayFormat("yyyy-MM-dd")
		end_date_edit.setCalendarPopup(True)
		end_date_edit.setDate(QDate.currentDate())

		date_layout.addWidget(start_label)
		date_layout.addWidget(start_date_edit)
		date_layout.addWidget(end_label)
		date_layout.addWidget(end_date_edit)

		layout.addRow(date_container)
		self.dynamic_filter_inputs["Start"] = start_date_edit
		self.dynamic_filter_inputs["End"] = end_date_edit

	def connect_actions(self):
		r"""
		Connect UI actions to corresponding methods.
		"""
		# actions for switch language
		self.ui.actionEnglish.triggered.connect(lambda: self.switch_language('english'))
		self.ui.actionGerman.triggered.connect(lambda: self.switch_language('german'))
		# actions for table setup (connect directory)
		self.ui.actionOpen.triggered.connect(self.open_setting_dialog)
		# activate, deactivate, select all actions
		self.ui.actionActive.triggered.connect(self.toggle_activation)
		self.ui.actionDeactive.triggered.connect(self.toggle_deactivation)
		self.ui.actionSelectAll.triggered.connect(self.table_operator.check_all_boxes)
		# actions for right side tool widget
		self.ui.actionFilter.triggered.connect(self.open_filter_widget)
		self.ui.actionInformation.triggered.connect(self.open_info_widget)
		self.ui.filterDockWidget.visibilityChanged.connect(self.ui.actionFilter.setChecked)
		self.ui.infoDockWidget.visibilityChanged.connect(self.ui.actionInformation.setChecked)
		self.ui.filterButton.clicked.connect(
			lambda: self.table_operator.filter_table(self.dynamic_filter_inputs)
		)
		self.ui.cancelButton.clicked.connect(
			lambda: self.table_operator.reset_filter(self.dynamic_filter_inputs)
		)
		self.ui.actionSearch.triggered.connect(self.open_search_widget)
		self.ui.searchDockWidget.visibilityChanged.connect(self.ui.actionSearch.setChecked)
		self.ui.actionRefresh.triggered.connect(self.setup_table)
		self.ui.actionNew.triggered.connect(self.table_operator.add_new_row)
		self.ui.actionDelete.triggered.connect(self.table_operator.delete_row)
		self.ui.actionRenameSensor.triggered.connect(self.rename_sensor_name)
		self.ui.actionExit.triggered.connect(self.exit_application)
		self.ui.actionDocumentation.triggered.connect(self.open_documentation)
		self.ui.actionUSBLoad.triggered.connect(self.keyfile_transfer)
		self.ui.actionExportKeyfiles.triggered.connect(self.keyfile_export)
		self.ui.actionAbout.triggered.connect(self.show_about_dialog)
		self.ui.actionSaveChange.triggered.connect(self.save_as_json)
		self.ui.actionEdit.triggered.connect(self.open_json_edit_dialog)
		self.ui.actionTableColumn.triggered.connect(self.open_column_configurator)

	def open_json_edit_dialog(self):
		checked_serial_numbers = self.get_checked_serial_numbers()
		if not checked_serial_numbers:
			QMessageBox.warning(self, self.tr("Error"), self.tr("No keyfile selected for edit."))
			return

		serial_number = checked_serial_numbers[0]
		metadata = self.folder_content.read_metadata(serial_number)

		dialog = MetadataEditor(serial_number, metadata, parent=self)
		if dialog.exec_() == QDialog.DialogCode.Accepted:
			updated_metadata = dialog.result_metadata
			self.folder_content.update_metadata(serial_number, updated_metadata)
			self.update_table_row([serial_number])
		self.reset_all_checkboxes()

	def open_column_configurator(self):

		dialog = ColumnConfigurator(self.custom_columns, parent=self)
		if dialog.exec_() == QDialog.DialogCode.Accepted:
			self.custom_columns = dialog.selected_columns

			self.config_manager.custom_columns = self.custom_columns
			self.config_manager.save_config()

			self.setup_table()
			self.setup_filter_dockwidget()

	def save_as_json(self):
		r"""
		Export non-empty, non-read-only table values from selected rows
		to a 'metadata.json' file inside the corresponding Keyfile directory.
		"""

		table = self.ui.tableWidget
		read_only_columns = [0, 1, 2, 3, 10, 11]

		for row in range(table.rowCount()):
			serial_number = table.item(row, 2).data(Qt.ItemDataRole.UserRole + 2)

			if self.check_activation_status(serial_number) == ActivationStatus.ACTIVATED:
				keyfile_path = os.path.join(self.directory1, serial_number)
			elif self.check_activation_status(serial_number) == ActivationStatus.DEACTIVATED:
				keyfile_path = os.path.join(self.directory2, serial_number)
			else:
				continue

			if not os.path.isdir(keyfile_path):
				continue

			meta_json_path = os.path.join(keyfile_path, "metadata.json")
			meta_data = {}

			if os.path.exists(meta_json_path):
				with open(meta_json_path, "r", encoding="utf-8") as f:
					try:
						existing_data = json.load(f)
					except json.JSONDecodeError:
						existing_data = {}
			else:
				existing_data = {}

			for col in range(table.columnCount()):
				if col in read_only_columns:
					continue

				item = table.item(row, col)
				column_name = table.horizontalHeaderItem(col).text()

				field_name = column_name

				if item and item.text().strip():
					meta_data[field_name] = item.text().strip()
				elif field_name in existing_data:
					del existing_data[field_name]

			existing_data.update(meta_data)

			with open(meta_json_path, "w", encoding="utf-8") as f:
				json.dump(existing_data, f, indent=4, ensure_ascii=False)

			# if existing_data:
			# 	with open(meta_json_path, "w", encoding="utf-8") as f:
			# 		json.dump(existing_data, f, indent=4, ensure_ascii=False)
			# elif os.path.exists(meta_json_path):
			# 	os.remove(meta_json_path)
		self.reset_all_checkboxes()

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
		dialog.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
		layout = QVBoxLayout(dialog)
		svg_logo = QSvgWidget(resource_path('resources/foskeyman_logo_long.svg'))
		layout.addWidget(svg_logo, alignment=Qt.AlignmentFlag.AlignCenter)
		info_label = QLabel(f"Version: {version}\nRelease Date: {release_date}")
		info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(info_label)
		author_label = QLabel(f"Authors:\nBertram Richter\nXiaoli Song")
		author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(author_label)
		copyright_label = QLabel(f"Copyright:\nInstitut für Massivbau\nTechnische Universität Dresden")
		copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(copyright_label)
		license_label = QLabel(
			"License:\nThis software is licensed under the GNU General Public License (GPL) Version 3, 29  June  2007."
			)
		license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
								QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
								)
							if user_choice == QMessageBox.StandardButton.Yes:
								shutil.rmtree(conflict_path)
							elif user_choice == QMessageBox.StandardButton.No:
								continue
						shutil.copytree(source_path, final_target_path, dirs_exist_ok=True)
				QMessageBox.information(self, "Success",
										f"All keyfile folders have been copied to deactivated directory.")
			except Exception as e:
				QMessageBox.critical(self, "Error", f"An error occurred: {e}")
		self.setup_table()

	def keyfile_export(self):
		r"""
		Export selected keyfiles from activated or deactivated directories to an external directory.
		Handle conflicts by allowing overwriting or skipping.
		"""
		checked_serial_numbers = self.get_checked_serial_numbers()
		if not checked_serial_numbers:
			QMessageBox.warning(self, self.tr("Error"), self.tr("No keyfile selected for export."))
			return

		export_path = QFileDialog.getExistingDirectory(self, self.tr("Select Export Directory"))
		if not export_path:
			return

		for serial_number in checked_serial_numbers:
			source_folder = None

			if self.check_activation_status(serial_number) == ActivationStatus.ACTIVATED:
				source_folder = os.path.join(self.directory1, serial_number)
			elif self.check_activation_status(serial_number) == ActivationStatus.DEACTIVATED:
				source_folder = os.path.join(self.directory2, serial_number)

			if source_folder and os.path.exists(source_folder):
				destination_folder = os.path.join(export_path, serial_number)

				if os.path.exists(destination_folder):
					user_choice = QMessageBox.question(
						self,
						self.tr("Conflict Detected"),
						self.tr(f"The folder '{serial_number}' already exists in the destination. Overwrite?"),
						QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
					)
					if user_choice == QMessageBox.StandardButton.Yes:
						shutil.rmtree(destination_folder)
					else:
						continue

				try:
					shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
					logging.info(f"Keyfile {serial_number} exported to {destination_folder}.")
				except Exception as e:
					QMessageBox.warning(self, self.tr("Error"),
										self.tr(f"Failed to export keyfile {serial_number}: {e}"))
			else:
				QMessageBox.warning(self, self.tr("Error"),
									self.tr(f"Source folder for keyfile {serial_number} does not exist."))

		QMessageBox.information(self, self.tr("Success"), self.tr("Selected keyfiles exported successfully."))
	
	def open_setting_dialog(self):
		r"""
		Open a dialog for selecting two directories.
		If valid, initialize KeyHandler and FolderContent, and save the paths to the config.json file.
		"""
		dialog = QDialog(self)
		open_ui = Ui_Open()
		open_ui.setupUi(dialog)
		self.config_manager.open_ui = open_ui
		open_ui.acBrowseButton.clicked.connect(lambda: self.config_manager.select_directory1(dialog, open_ui))
		open_ui.deacBrowseButton.clicked.connect(lambda: self.config_manager.select_directory2(dialog, open_ui))

		dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
		dialog.setWindowTitle(self.tr("Directory Settings"))
		# Pre-fill the input fields if the directories have already been selected previously
		if self.directory1 and self.directory2:
			open_ui.acLineEdit.setText(self.directory1)
			open_ui.deacLineEdit.setText(self.directory2)

		open_ui.confirmButton.clicked.connect(lambda: self.config_manager.confirm_directory_selection(dialog, open_ui))
		open_ui.cancelButton.clicked.connect(dialog.reject)
		if dialog.exec_():
			if self.config_manager.directory1 and self.config_manager.directory2:
				self.directory1 = self.config_manager.directory1
				self.directory2 = self.config_manager.directory2
				self.config_manager.save_config()
				self.initialize_handlers()
	
	def initialize_handlers(self):
		r"""
		Initialize KeyHandler and FolderContent based on the selected directory paths.
		If success, set up the table for further operations.
		"""
		self.key_handler = KeyHandler(self.directory1, self.directory2)
		if not self.key_handler.check_directories():
			QMessageBox.warning(self, "Error", self.tr("Directory validation failure"))
			return
		self.folder_content = FolderContent(self.directory1, self.directory2)
		self.setup_table()

	def rename_sensor_name(self):
		r"""
		Rename the sensor name. Only work for the first selected entry.
		"""
		serial_numbers = self.get_checked_serial_numbers()
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
			if dialog.exec_() == QDialog.DialogCode.Accepted:
				new_name = dialog.get_new_sensor_name()
				self.folder_content.edit_sensor_name_for_key(serial_number, new_name)
				logging.info(f"Sensor name updated for Serial Number {serial_number}: {sensor_name} -> {new_name}")
				self.update_table_row([serial_number])
		self.reset_all_checkboxes()
	
	def check_activation_status(self, serial_number):
		r"""
		Check the activation status for a given serial number.
		\param serial_number (str): The serial number to check.
		\return (ActivationStatus): The activation status of the given serial number, or None if not found.
		"""
		for row in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.item(row, 2).data(Qt.ItemDataRole.UserRole + 2) == serial_number:
				activation_item = self.ui.tableWidget.item(row, 1)
				activation_status = activation_item.data(Qt.ItemDataRole.UserRole + 1)
				return activation_status
		return None
	
	def get_checked_serial_numbers(self):
		r"""Retrieve serial numbers for rows where the checkbox is checked.	"""
		serial_numbers = []
		for row in range(self.ui.tableWidget.rowCount()):
			checkbox_item = self.ui.tableWidget.item(row, 0)
			if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
				serial_number = self.ui.tableWidget.item(row, 2).data(Qt.ItemDataRole.UserRole + 2)
				serial_numbers.append(serial_number)
		return serial_numbers
	
	def reset_all_checkboxes(self):
		r"""Reset all checkboxes in the table to an unchecked state."""
		for row in range(self.ui.tableWidget.rowCount()):
			checkbox_item = self.ui.tableWidget.item(row, 0)
			if checkbox_item and checkbox_item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
				checkbox_item.setCheckState(Qt.CheckState.Unchecked)
	
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
		if self.ui.tableWidget.item(row, 2).data(Qt.ItemDataRole.UserRole + 2) is None:
			return
		serial_number = self.ui.tableWidget.item(row, 2).data(Qt.ItemDataRole.UserRole + 2)
		user_properties = self.folder_content.read_user_properties(serial_number)
		gage_segment = self.folder_content.read_gage_segment(serial_number)
		od6ref_file = self.folder_content.read_od6ref_file(serial_number)
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
		Populate table with data in metadata.json, and connect a cell click event to display additional information.
		"""
		fixed_columns = [
			' ',
			self.tr('Status'),
			self.tr('Serial Number'),
			self.tr('Sensor Name')
		]

		custom_columns = self.custom_columns

		fixed_tail_columns = [
			self.tr('Last Edit Date'),
			self.tr('Sensor Length (m)')
		]

		all_columns = fixed_columns + [self.tr(col) for col in custom_columns] + fixed_tail_columns

		self.ui.tableWidget.setColumnCount(len(all_columns))
		self.ui.tableWidget.setHorizontalHeaderLabels(all_columns)

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
		""")
		self.ui.tableWidget.setColumnWidth(0, 10)
		self.ui.tableWidget.setColumnWidth(1, 180)

		header = self.ui.tableWidget.horizontalHeader()
		header.setSectionsMovable(True)
		header.setDragEnabled(True)
		header.setDragDropMode(QHeaderView.DragDropMode.DragDrop)

		if self.key_handler is None:
			return

		self.ui.tableWidget.setRowCount(0)
		self.populate_table()

		read_only_indices = [1, 2, 3] + [len(all_columns) - 2, len(all_columns) - 1]
		self.set_columns_read_only(read_only_indices)
		self.set_columns_background_color([2, 3, len(all_columns) - 2, len(all_columns) - 1])

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
					item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
	
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
		self.ui.tableWidget.setSortingEnabled(False)

		activated_keys = set(self.key_handler.read_keys('activated'))
		deactivated_keys = set(self.key_handler.read_keys('deactivated'))

		keys_with_status = [(key, "Activated") for key in activated_keys] + \
						   [(key, "Deactivated") for key in deactivated_keys]

		self.ui.tableWidget.setRowCount(len(keys_with_status))

		for row_idx, (key, status) in enumerate(keys_with_status):
			total_cols = self.ui.tableWidget.columnCount()

			for col in range(total_cols):
				if self.ui.tableWidget.item(row_idx, col) is None:
					self.ui.tableWidget.setItem(row_idx, col, QTableWidgetItem())

			if status == 'Activated':
				activation_status = ActivationStatus.ACTIVATED
				self.ui.tableWidget.setCellWidget(row_idx, 1, self.create_status_button('Activated'))
			else:
				activation_status = ActivationStatus.DEACTIVATED
				self.ui.tableWidget.setCellWidget(row_idx, 1, self.create_status_button('Deactivated'))

			activation_item = self.ui.tableWidget.item(row_idx, 1)
			activation_item.setData(Qt.ItemDataRole.DisplayRole, activation_status.value)
			activation_item.setForeground(Qt.GlobalColor.transparent)
			activation_item.setData(Qt.ItemDataRole.UserRole + 1, activation_status)

			check_item = self.ui.tableWidget.item(row_idx, 0)
			check_item.setCheckState(Qt.CheckState.Unchecked)

			metadata = self.folder_content.read_metadata(key)

			self.ui.tableWidget.item(row_idx, 2).setText(key)
			self.ui.tableWidget.item(row_idx, 2).setData(Qt.ItemDataRole.UserRole + 2, key)

			self.ui.tableWidget.item(row_idx, 3).setText(self.folder_content.read_sensor_name_for_key(key))

			edit_date = self.folder_content.get_last_edit_date(key)
			edit_date_str = edit_date.strftime("%Y-%m-%d") if edit_date else ""

			last_edit_idx = self.ui.tableWidget.columnCount() - 2
			sensor_len_idx = self.ui.tableWidget.columnCount() - 1

			self.ui.tableWidget.item(row_idx, last_edit_idx).setText(edit_date_str)

			sensor_length = self.folder_content.read_sensor_length_for_key(key)
			sensor_length_str = str(sensor_length) if sensor_length is not None else ""
			self.ui.tableWidget.item(row_idx, sensor_len_idx).setText(sensor_length_str)

			for i, col_name in enumerate(self.custom_columns):
				col_idx = 4 + i
				value = metadata.get(col_name, "")
				self.ui.tableWidget.item(row_idx, col_idx).setText(value)

		self.ui.tableWidget.setSortingEnabled(True)

	def create_status_button(self, status):
		r"""
		Creates a colored QPushButton based on its activation status.
		The button will be colored differently depending on whether the status is 'Activated' or
		'Deactivated'. The button is not clickable and will display the status text.
		\param status (str): The activation status ('Activated', 'Deactivated').
		\return (QWidget): A QWidget containing the styled QPushButton for status display.
		"""
		status_translation_map = {
			'Activated': self.tr("Activated"),
			'Deactivated': self.tr("Deactivated"),
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

		container = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(button)
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.setContentsMargins(0, 0, 0, 0)
		container.setLayout(layout)
		return container
	
	def toggle_activation(self):
		r"""
		Activate the selected items (checkbox is checked) in the table.
		For valid items, the keyfile moved from deactivated directory to activate directory.
		Upon successful activation, the item's status is updated to 'Activated' and the status button is turn green.
		"""
		for i in range(self.ui.tableWidget.rowCount()):
			check_item = self.ui.tableWidget.item(i, 0)
			activation_item = self.ui.tableWidget.item(i, 1)
			serial_number = self.ui.tableWidget.item(i, 2).data(Qt.ItemDataRole.UserRole + 2)
			if check_item.checkState() == Qt.CheckState.Checked:
				success = self.key_handler.activate_key(serial_number)
				if success:
					activation_item.setData(Qt.ItemDataRole.UserRole + 1, ActivationStatus.ACTIVATED)
					self.ui.tableWidget.setCellWidget(i, 1, self.create_status_button('Activated'))
				check_item.setCheckState(Qt.CheckState.Unchecked)
	
	def toggle_deactivation(self):
		r"""
		Deactivate the selected item (checkbox is checked) in the table.
		For valid items, the keyfile moved from the activated directory to the deactivated directory.
		Upon successful deactivation, the item's status is updated to 'Deactivated', and the status button turns grey.
		"""
		for i in range(self.ui.tableWidget.rowCount()):
			check_item = self.ui.tableWidget.item(i, 0)
			activation_item = self.ui.tableWidget.item(i, 1)
			serial_number = self.ui.tableWidget.item(i, 2).data(Qt.ItemDataRole.UserRole + 2)
			if check_item.checkState() == Qt.CheckState.Checked:
				success = self.key_handler.deactivate_key(serial_number)
				if success:
					activation_item.setData(Qt.ItemDataRole.UserRole + 1, ActivationStatus.DEACTIVATED)
					self.ui.tableWidget.setCellWidget(i, 1, self.create_status_button('Deactivated'))
				check_item.setCheckState(Qt.CheckState.Unchecked)
	
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
		self.save_current_column_order()
		QCoreApplication.instance().quit()

	def closeEvent(self, event):
		"""Triggered when user clicks X to close the window."""
		self.save_current_column_order()
		event.accept()

	def save_current_column_order(self):
		header = self.ui.tableWidget.horizontalHeader()
		total_columns = self.ui.tableWidget.columnCount()

		ordered_column_names = []
		for visual_pos in range(total_columns):
			logical_index = header.logicalIndex(visual_pos)
			header_item = self.ui.tableWidget.horizontalHeaderItem(logical_index)
			if header_item:
				column_name = header_item.text()
				ordered_column_names.append(column_name)

		ordered_custom_columns = []
		for name in ordered_column_names:
			if name in self.custom_columns:
				ordered_custom_columns.append(name)

		self.custom_columns = ordered_custom_columns
		self.config_manager.custom_columns = self.custom_columns
		self.config_manager.save_config()

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
			serial_number = self.ui.tableWidget.item(row, 2).data(Qt.ItemDataRole.UserRole + 2)
			if serial_number:
				keyfiles.add(serial_number)
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
				item = self.ui.tableWidget.item(row, 2)
				if item and item.data(Qt.ItemDataRole.UserRole + 2) == serial_number:
					row_index = row
					break

			if row_index is None:
				continue

			if serial_number in self.key_handler.read_keys('activated'):
				activation_status = ActivationStatus.ACTIVATED
				self.ui.tableWidget.setCellWidget(row_index, 1, self.create_status_button('Activated'))
			elif serial_number in self.key_handler.read_keys('deactivated'):
				activation_status = ActivationStatus.DEACTIVATED
				self.ui.tableWidget.setCellWidget(row_index, 1, self.create_status_button('Deactivated'))
			else:
				continue

			activation_item = self.ui.tableWidget.item(row_index, 1)
			activation_item.setData(Qt.ItemDataRole.UserRole + 1, activation_status)

			check_item = self.ui.tableWidget.item(row_index, 0)
			check_item.setCheckState(Qt.CheckState.Unchecked)

			metadata = self.folder_content.read_metadata(serial_number)

			self.ui.tableWidget.item(row_index, 2).setText(serial_number)
			self.ui.tableWidget.item(row_index, 2).setData(Qt.ItemDataRole.UserRole + 2, serial_number)

			self.ui.tableWidget.item(row_index, 3).setText(self.folder_content.read_sensor_name_for_key(serial_number))

			edit_date = self.folder_content.get_last_edit_date(serial_number)
			edit_date_str = edit_date.strftime("%Y-%m-%d") if edit_date else ""
			last_edit_idx = self.ui.tableWidget.columnCount() - 2
			self.ui.tableWidget.item(row_index, last_edit_idx).setText(edit_date_str)

			sensor_length = self.folder_content.read_sensor_length_for_key(serial_number)
			sensor_length_str = str(sensor_length) if sensor_length is not None else ""
			sensor_len_idx = self.ui.tableWidget.columnCount() - 1
			self.ui.tableWidget.item(row_index, sensor_len_idx).setText(sensor_length_str)

			if metadata:
				for i, col_name in enumerate(self.custom_columns):
					col_idx = 4 + i
					value = metadata.get(col_name, "")
					self.ui.tableWidget.item(row_index, col_idx).setText(value)


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


def main():
	r"""Initialize and run the application."""
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show_and_check_config()
	sys.exit(app.exec_())

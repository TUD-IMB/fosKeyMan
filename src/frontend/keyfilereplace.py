import io
import logging
import os
import zipfile
import json
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from frontend.ui.uireplace import Ui_Replace
from utils.utils import format_json_to_html


class KeyfileReplace(QDialog):
	"""
	A dialog window for handling keyfile mismatches between the database and disk.
	"""
	def __init__(self, serial_numbers, db_handler, disk_file_paths, is_batch_mode=False, parent=None):
		r"""
		Initialize the KeyfileReplace dialog with the given serial numbers, database handler, and file paths on disk.

		\param serial_numbers (list): A list of serial numbers used to identify keyfiles.
		\param db_handler (DatabaseHandler): The handler for managing database interactions.
		\param disk_file_paths (list): A list of paths to keyfiles on disk corresponding to the serial numbers.
		\param is_batch_mode (bool): If True, enable batch mode to process multiple keyfiles sequentially.
		\param parent (QWidget, optional): The parent widget for this dialog.
		"""
		super(KeyfileReplace, self).__init__(parent)

		self.serial_numbers = serial_numbers
		self.disk_file_paths = disk_file_paths
		self.db_handler = db_handler
		self.is_batch_mode = is_batch_mode
		self.current_index = 0
		self.db_blob = self.db_handler.get_blob_data(self.serial_numbers[self.current_index])

		self.ui = Ui_Replace()
		self.ui.setupUi(self)
		self.resize(2000, 1000)
		self.setWindowTitle(self.tr("Mismatch detected in Keyfiles"))

		self.ui.dbTreeView.setModel(QStandardItemModel())
		self.ui.diskTreeView.setModel(QStandardItemModel())
		self.ui.saveButton.clicked.connect(self.replace_keyfile)

		self.load_tree_views()

		self.ui.dbTreeView.clicked.connect(self.on_file_selected)
		self.ui.diskTreeView.clicked.connect(self.on_file_selected)

		if self.is_batch_mode:
			self.skipButton = QPushButton(self.tr("Skip"), self)
			self.ui.horizontalButtonlLayout.addWidget(self.skipButton)
			self.skipButton.clicked.connect(self.next_replace_keyfile)

			self.finishButton = QPushButton(self.tr("Finish"), self)
			self.ui.horizontalButtonlLayout.addWidget(self.finishButton)
			self.finishButton.clicked.connect(self.accept)

		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

	def next_replace_keyfile(self):
		r"""In batch mode, move to the next record when "Skip" is clicked."""
		if self.current_index >= len(self.serial_numbers) - 1:
			self.accept()
			return

		self.current_index += 1
		self.update_current_keyfile_info()

		if self.current_index == len(self.serial_numbers) - 1:
			self.skipButton.setDisabled(True)

	def update_current_keyfile_info(self):
		r"""Update the dialog to show information for the current keyfile in batch mode."""
		self.db_blob = self.db_handler.get_blob_data(self.serial_numbers[self.current_index])
		self.load_tree_views()

	def replace_keyfile(self):
		r"""
		Replace the keyfile in the database or on disk based on the user's selection.

		- If the user selects the database option (`dbRadioButton`), the keyfile stored in the database is fetched
		and saved to the disk, replacing the keyfile on the disk.
		- If the user selects the disk option (`diskRadioButton`), the keyfile from the disk is uploaded to the database,
		replacing the keyfile in the corresponding database record.
		"""
		try:
			if self.ui.dbRadioButton.isChecked():
				output_file_path = self.disk_file_paths[self.current_index]
				self.db_handler.fetch_blob_and_save_as_folder(self.serial_numbers[self.current_index], output_file_path)
				logging.info(
					f"Replaced disk keyfile with the database version, file path: {output_file_path}"
				)
			elif self.ui.diskRadioButton.isChecked():
				folder_path = self.disk_file_paths[self.current_index]
				zip_buffer = self.db_handler.create_zip_from_folder(folder_path)
				self.db_handler.update_blob_data(zip_buffer.getvalue(), self.serial_numbers[self.current_index])
				self.db_handler.commit()
				logging.info(
					f"Replaced database keyfile with the disk version, file path: {folder_path}"
				)
			else:
				self.ui.textBrowser.setPlainText(self.tr("Please select a keyfile version to keep."))
				return

			if self.current_index == len(self.serial_numbers) - 1:
				self.accept()
			else:
				self.next_replace_keyfile()

		except Exception as e:
			self.ui.textBrowser.setPlainText(
				self.tr("Error occurred during replace operation: {error}").format(error=e)
			)

	def load_tree_views(self):
		r"""
		Display the directory structure of the keyfile from both the database (BLOB) and the disk.
		Extract file names from the keyfiles and display them in tree views for comparison.
		"""
		try:

			db_zip_bytes = io.BytesIO(self.db_blob)
			with zipfile.ZipFile(db_zip_bytes, 'r') as db_zip:
				db_files = set(db_zip.namelist())

			disk_files = set()
			for root, dirs, files in os.walk(self.disk_file_paths[self.current_index]):
				for file in files:
					file_path = os.path.join(root, file)
					relative_path = os.path.relpath(file_path, start=self.disk_file_paths[self.current_index])
					disk_files.add(relative_path.replace("\\", "/"))

			self.ui.dbTreeView.model().clear()
			self.ui.diskTreeView.model().clear()

			self.ui.dbTreeView.header().hide()
			self.ui.diskTreeView.header().hide()

			for file_name in db_files:
				self.add_tree_item(self.ui.dbTreeView.model(), file_name)

			for file_name in disk_files:
				self.add_tree_item(self.ui.diskTreeView.model(), file_name)

		except Exception as e:
			self.ui.textBrowser.setPlainText(
				self.tr("Error occurred: {error}").format(error=e)
			)

	def add_tree_item(self, model, file_name):
		r"""
		Insert files or directories into a QStandardItemModel based on the file path.
		Directories are added as parent items, and files are added as child items.

		\param model (QStandardItemModel): The model to which the file or directory will be added (db or disk).
		\param file_name (str): The full file path, where directories are separated by '/'.
		"""
		parts = file_name.split('/')
		parent_item = model.invisibleRootItem()

		# directory
		for part in parts[:-1]:
			if part.strip() == "":
				continue

			found_items = []
			for i in range(parent_item.rowCount()):
				if parent_item.child(i).text() == part:
					found_items.append(parent_item.child(i))

			if found_items:
				parent_item = found_items[0]
			else:
				dir_item = QStandardItem(part)
				parent_item.appendRow([dir_item])
				parent_item = dir_item

		# file
		if parts[-1].strip() != "":
			file_item = QStandardItem(parts[-1])
			parent_item.appendRow([file_item])

	def on_file_selected(self, index):
		r"""
		Display the content of the selected file in the text browser when the user selects a file.

		\param index (QModelIndex): The index of the selected item in the tree view.
		"""
		selected_item = self.sender().model().itemFromIndex(index)
		file_name = selected_item.text()

		if self.sender() == self.ui.dbTreeView:
			zip_source = "database"
		else:
			zip_source = "disk"

		try:

			if zip_source == "database":
				try:
					blob_stream = io.BytesIO(self.db_blob)
					with zipfile.ZipFile(blob_stream, 'r') as zip_file:
						if file_name in zip_file.namelist():
							with zip_file.open(file_name) as file:
								first_line = file.readline().decode('utf-8', errors='ignore').strip()
								try:
									json_data = json.dumps(json.loads(first_line), indent=4, ensure_ascii=False)
									formatted_json = format_json_to_html(json_data)
									self.ui.textBrowser.setHtml(formatted_json)
								except json.JSONDecodeError:
									self.ui.textBrowser.setPlainText(first_line)
						else:
							self.ui.textBrowser.setPlainText("")
				except Exception as e:
					self.ui.textBrowser.setPlainText(self.tr("Error reading file content: {error}").format(error=e))

			else:
				full_path = os.path.join(self.disk_file_paths[self.current_index], file_name)
				if os.path.isdir(full_path):
					self.ui.textBrowser.setPlainText("")
				elif os.path.exists(full_path):
					with open(full_path, 'r', encoding='utf-8', errors='ignore') as disk_file:
						first_line = disk_file.readline().strip()
						try:
							json_data = json.dumps(json.loads(first_line), indent=4, ensure_ascii=False)
							formatted_json = format_json_to_html(json_data)
							self.ui.textBrowser.setHtml(formatted_json)
						except json.JSONDecodeError:
							self.ui.textBrowser.setPlainText(first_line)
		except Exception as e:
			self.ui.textBrowser.setPlainText(
				self.tr("Error reading file content: {error}").format(error=e))


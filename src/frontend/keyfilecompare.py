import json
import io
import zipfile
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from frontend.ui.uicompare import Ui_Compare
from utils.utils import format_json_to_html


class KeyfileCompare(QDialog):
	"""
	A dialog window for comparing two BLOB keyfile contents, similar to KeyfileReplace.
	"""

	def __init__(self, current_blob, imported_blob, parent=None):
		r"""
		Initialize the KeyfileCompare dialog with two BLOB data inputs for comparison.

		\param current_blob (bytes): The BLOB data for the current keyfile.
		\param imported_blob (bytes): The BLOB data for the imported keyfile.
		\param parent (QWidget, optional): The parent widget for this dialog.
		"""
		super(KeyfileCompare, self).__init__(parent)

		self.current_blob = current_blob
		self.imported_blob = imported_blob

		self.selected_version = None

		self.ui = Ui_Compare()
		self.ui.setupUi(self)
		self.resize(2000, 1000)
		self.setWindowTitle(self.tr("Compare Keyfiles"))

		self.ui.currentTreeView.setModel(QStandardItemModel())
		self.ui.importedTreeView.setModel(QStandardItemModel())
		self.ui.closeButton.clicked.connect(self.close_dialog)

		self.load_tree_views()

		self.ui.currentTreeView.clicked.connect(self.on_file_selected)
		self.ui.importedTreeView.clicked.connect(self.on_file_selected)

		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

	def load_tree_views(self):
		r"""
		Display the directory structure of the keyfiles from both current and imported BLOBs.
		"""
		try:
			current_model = self.ui.currentTreeView.model()
			current_model.clear()
			if self.current_blob:
				blob_stream = io.BytesIO(self.current_blob)
				with zipfile.ZipFile(blob_stream, 'r') as zip_file:
					for file_name in zip_file.namelist():
						self.add_tree_item(current_model, file_name)
			else:
				root_item = QStandardItem(self.tr("Current Keyfile (No attached Keyfile)"))
				current_model.appendRow(root_item)

			imported_model = self.ui.importedTreeView.model()
			imported_model.clear()
			if self.imported_blob:
				blob_stream = io.BytesIO(self.imported_blob)
				with zipfile.ZipFile(blob_stream, 'r') as zip_file:
					for file_name in zip_file.namelist():
						self.add_tree_item(imported_model, file_name)
			else:
				root_item = QStandardItem(self.tr("Imported Keyfile (No attached Keyfile)"))
				imported_model.appendRow(root_item)

			self.ui.currentTreeView.header().hide()
			self.ui.importedTreeView.header().hide()

		except Exception as e:
			self.ui.textBrowser.setPlainText(
				self.tr("Error occurred: {error}").format(error=e)
			)

	def add_tree_item(self, model, file_name):
		r"""
		Inserts file paths into a QStandardItemModel based on the file structure.

		\param model (QStandardItemModel): The model to which the file or directory will be added (current or imported).
		\param file_name (str): The full file path, where directories are separated by '/'.
		"""
		parts = file_name.split('/')
		parent_item = model.invisibleRootItem()

		for part in parts[:-1]:
			if part.strip() == "":
				continue

			found_item = None
			for i in range(parent_item.rowCount()):
				if parent_item.child(i).text() == part:
					found_item = parent_item.child(i)
					break

			if found_item:
				parent_item = found_item
			else:
				dir_item = QStandardItem(part)
				parent_item.appendRow([dir_item])
				parent_item = dir_item

		if parts[-1].strip() != "":
			file_item = QStandardItem(parts[-1])
			parent_item.appendRow([file_item])

	def on_file_selected(self, index):
		r"""
		Display the content of the selected file in the text browser.

		\param index (QModelIndex): The index of the selected item in the tree view.
		"""
		selected_item = self.sender().model().itemFromIndex(index)
		file_name = selected_item.text()

		if self.sender() == self.ui.currentTreeView:
			blob_data = self.current_blob
		else:
			blob_data = self.imported_blob

		try:
			blob_stream = io.BytesIO(blob_data)
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

	def close_dialog(self):
		r"""Close the current dialog window."""
		self.close()


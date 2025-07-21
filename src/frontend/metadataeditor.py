from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QPushButton, QTableWidgetItem, QMessageBox, QSizePolicy, QHeaderView
from frontend.ui.uiedit import Ui_Edit
import frontend.ui.toolicons_rc
from utils.utils import apply_icon_button_style


class MetadataEditor(QDialog):
	r"""
	Class to edit the metadata.json contents for selected keyfiles.
	"""

	def __init__(self, serial_numbers, metadata_list, parent=None):
		r"""
		Initialize the MetadataEditor dialog.

		\param serial_numbers (list): List of serial numbers for the keyfiles.
		\param metadata_list (list): List of metadata dictionaries corresponding to each serial number.
		\param parent (QWidget, optional): Parent widget for this dialog.
		"""
		super(MetadataEditor, self).__init__(parent)

		self.serial_numbers = serial_numbers
		self.metadata_list = metadata_list
		self.current_index = 0
		self.result_metadata = {}
		self.serial_number = self.serial_numbers[self.current_index]
		self.original_metadata = self.metadata_list[self.current_index]

		self.ui = Ui_Edit()
		self.ui.setupUi(self)

		self.ui.cancelButton.clicked.connect(self.reject)
		self.ui.confirmButton.clicked.connect(self.confirm_or_next)

		self.load_metadata(self.current_index)

	def load_metadata(self, index):
		r"""
		Load metadata for the given index into the editor UI.

		\param index (int): Index of the serial number and metadata to load.
		"""
		self.clear_table()

		self.serial_number = self.serial_numbers[index]
		self.original_metadata = self.metadata_list[index]

		self.ui.keyLabel.setText(self.tr("Serial Number: ") + self.serial_number)

		self.setup_main_table()
		self.setup_add_table()

		if index == len(self.serial_numbers) - 1:
			self.ui.confirmButton.setText(self.tr("Confirm"))
		else:
			self.ui.confirmButton.setText(self.tr("Next"))

	def clear_table(self):
		r"""
		Clear all rows and content from the metadata table before loading next one.
		"""
		self.ui.tableWidget.clearContents()
		self.ui.tableWidget.setRowCount(0)

	def setup_main_table(self):
		r"""
		Set up the main table to display and edit existing metadata entries.
		"""
		self.ui.tableWidget.setColumnCount(3)
		self.ui.tableWidget.setHorizontalHeaderLabels(["Property", "Value", ""])
		self.ui.tableWidget.horizontalHeader().setStretchLastSection(False)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
		self.ui.tableWidget.setColumnWidth(2, 40)

		for key, value in self.original_metadata.items():
			self.insert_json_row(key, value)

	def setup_add_table(self):
		r"""
		Set up a small input table for adding new metadata key-value pairs.
		"""
		self.ui.addTableWidget.setColumnCount(3)
		self.ui.addTableWidget.setRowCount(1)
		self.ui.addTableWidget.horizontalHeader().setVisible(False)
		self.ui.addTableWidget.verticalHeader().setVisible(False)

		self.ui.addTableWidget.horizontalHeader().setStretchLastSection(False)
		self.ui.addTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		self.ui.addTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
		self.ui.addTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
		self.ui.addTableWidget.setColumnWidth(2, 40)

		row_height = self.ui.addTableWidget.verticalHeader().defaultSectionSize()
		self.ui.addTableWidget.setFixedHeight(row_height + 2)

		self.ui.addTableWidget.setItem(0, 0, QTableWidgetItem())
		self.ui.addTableWidget.setItem(0, 1, QTableWidgetItem())

		add_button = QPushButton()
		add_button.setIcon(QIcon(":/icons/icons/propertyadd.svg"))
		apply_icon_button_style(add_button)
		add_button.setIconSize(QSize(20, 20))
		add_button.setFixedSize(24, 24)
		add_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		self.ui.addTableWidget.setCellWidget(0, 2, add_button)

		add_button.clicked.connect(self.add_new_row)

	def insert_json_row(self, key, value):
		r"""
		Insert a new key-value pair as a row into the main metadata table.
		"""
		row_position = self.ui.tableWidget.rowCount()
		self.ui.tableWidget.insertRow(row_position)

		self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(key))
		self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(value))

		delete_button = QPushButton("")
		delete_button.setIcon(QIcon(":/icons/icons/editbin.svg"))
		apply_icon_button_style(delete_button)
		delete_button.setIconSize(QSize(20, 20))
		delete_button.setFixedSize(24, 24)
		delete_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		delete_button.clicked.connect(self.delete_current_row)
		self.ui.tableWidget.setCellWidget(row_position, 2, delete_button)

	def delete_current_row(self):
		r"""
		Find the row where the clicked button is located and delete it
		"""
		button = self.sender()
		if not button:
			return

		for row in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.cellWidget(row, 2) == button:
				self.ui.tableWidget.removeRow(row)
				break

	def add_new_row(self):
		r"""
		Add a new metadata entry from the input fields to the main table.
		"""
		key_item = self.ui.addTableWidget.item(0, 0)
		value_item = self.ui.addTableWidget.item(0, 1)

		key = key_item.text().strip() if key_item else ''
		value = value_item.text().strip() if value_item else ''

		if key and value:
			self.insert_json_row(key, value)
			self.ui.addTableWidget.setItem(0, 0, QTableWidgetItem())
			self.ui.addTableWidget.setItem(0, 1, QTableWidgetItem())
		else:
			QMessageBox.warning(self, self.tr("Input Error"), self.tr("Both Property and Value must be filled."))

	def confirm_or_next(self):
		r"""
		Switch to next one or if it's the last one it will confirm the changes and close the editor dialog.
		"""
		updated_metadata = {}
		for row in range(self.ui.tableWidget.rowCount()):
			key_item = self.ui.tableWidget.item(row, 0)
			value_item = self.ui.tableWidget.item(row, 1)
			if key_item and value_item:
				updated_metadata[key_item.text()] = value_item.text()

		current_serial = self.serial_numbers[self.current_index]
		self.result_metadata[current_serial] = updated_metadata

		if self.current_index == len(self.serial_numbers) - 1:
			self.accept()
		else:
			self.current_index += 1
			self.load_metadata(self.current_index)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView

from frontend.ui.uitrash import Ui_Trash


class TrashManager(QDialog):
	def __init__(self, key_handler, parent=None):
		super().__init__(parent)

		self.ui = Ui_Trash()
		self.ui.setupUi(self)

		self.key_handler = key_handler

		self.ui.closeButton.clicked.connect(self.reject)
		self.ui.emptyButton.clicked.connect(self.clear_all_trash)

		self.setup_trash_table()

	def setup_trash_table(self):
		self.ui.tableWidget.setRowCount(0)
		self.ui.tableWidget.setColumnCount(3)
		self.ui.tableWidget.setHorizontalHeaderLabels([self.tr("Serial Number"), "", ""])

		header = self.ui.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
		header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
		self.ui.tableWidget.setColumnWidth(1, 40)
		self.ui.tableWidget.setColumnWidth(2, 40)

		serial_numbers = self.key_handler.read_keys("trash")

		for serial_number in serial_numbers:
			row = self.ui.tableWidget.rowCount()
			self.ui.tableWidget.insertRow(row)

			item = QTableWidgetItem(serial_number)
			item.setFlags(Qt.ItemFlag.ItemIsEnabled)
			self.ui.tableWidget.setItem(row, 0, item)

			delete_btn = QPushButton()
			delete_btn.setToolTip(self.tr("Permanently delete"))
			delete_btn.setIcon(QIcon(":/icons/icons/editbin.svg"))
			delete_btn.setFixedSize(28, 28)
			delete_btn.setIconSize(QSize(20, 20))
			delete_btn.clicked.connect(lambda _, key=serial_number: self.delete_keyfile(key))
			self.ui.tableWidget.setCellWidget(row, 1, delete_btn)

			undo_btn = QPushButton()
			undo_btn.setToolTip(self.tr("Restore"))
			undo_btn.setIcon(QIcon(":/icons/icons/undo.svg"))
			undo_btn.setFixedSize(28, 28)
			undo_btn.setIconSize(QSize(20, 20))
			undo_btn.clicked.connect(lambda _, key=serial_number: self.restore_keyfile(key))
			self.ui.tableWidget.setCellWidget(row, 2, undo_btn)

	def clear_all_trash(self):
		confirm = QMessageBox.question(
			self,
			self.tr("Confirm Deletion"),
			self.tr("Are you sure you want to permanently delete all keyfiles in trash?"),
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		if confirm != QMessageBox.StandardButton.Yes:
			return

		for key in self.key_handler.read_keys("trash"):
			self.key_handler.permanently_delete_key(key)

		self.ui.tableWidget.setRowCount(0)

		QMessageBox.information(self, self.tr("Success"), self.tr("Trash has been cleared."))

	def delete_keyfile(self, key):
		if self.key_handler.permanently_delete_key(key):
			for row in range(self.ui.tableWidget.rowCount()):
				item = self.ui.tableWidget.item(row, 0)
				if item and item.text() == key:
					self.ui.tableWidget.removeRow(row)
					break

	def restore_keyfile(self, key):
		if self.key_handler.undo_delete_key(key):
			for row in range(self.ui.tableWidget.rowCount()):
				item = self.ui.tableWidget.item(row, 0)
				if item and item.text() == key:
					self.ui.tableWidget.removeRow(row)
					break


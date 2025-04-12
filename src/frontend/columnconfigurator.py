from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QPushButton, QSizePolicy, QMessageBox

from frontend.ui.uicolumn import Ui_Column
from utils.utils import apply_icon_button_style


class ColumnConfigurator(QDialog):
	def __init__(self, initial_columns, parent=None):
		super(ColumnConfigurator, self).__init__(parent)
		self.setWindowTitle(self.tr("Configure Table Columns"))

		self.ui = Ui_Column()
		self.ui.setupUi(self)

		self.initial_columns = initial_columns
		self.selected_columns = initial_columns.copy()

		self.setup_main_table()
		self.setup_add_table()

		self.ui.cancelButton.clicked.connect(self.reject)
		self.ui.confirmButton.clicked.connect(self.confirm_and_close)

	def setup_main_table(self):
		self.ui.tableWidget.setColumnCount(2)
		self.ui.tableWidget.setHorizontalHeaderLabels([self.tr("Column Name"), ""])
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
		self.ui.tableWidget.setColumnWidth(1, 40)

		for col_name in self.selected_columns:
			self.insert_column_row(col_name)

	def setup_add_table(self):
		self.ui.addTableWidget.setColumnCount(2)
		self.ui.addTableWidget.setRowCount(1)
		self.ui.addTableWidget.horizontalHeader().setVisible(False)
		self.ui.addTableWidget.verticalHeader().setVisible(False)
		self.ui.addTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		self.ui.addTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
		self.ui.addTableWidget.setColumnWidth(1, 40)

		row_height = self.ui.addTableWidget.verticalHeader().defaultSectionSize()
		self.ui.addTableWidget.setFixedHeight(row_height + 2)

		self.ui.addTableWidget.setItem(0, 0, QTableWidgetItem())

		add_button = QPushButton()
		add_button.setIcon(QIcon(":/icons/icons/editadd.svg"))
		apply_icon_button_style(add_button)
		add_button.setIconSize(QSize(20, 20))
		add_button.setFixedSize(24, 24)
		add_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		self.ui.addTableWidget.setCellWidget(0, 1, add_button)

		add_button.clicked.connect(self.add_new_column)

	def add_new_column(self):
		item = self.ui.addTableWidget.item(0, 0)
		col_name = item.text().strip() if item else ""
		if col_name:
			self.insert_column_row(col_name)
			self.ui.addTableWidget.setItem(0, 0, QTableWidgetItem())
		else:
			QMessageBox.warning(self, self.tr("Input Error"), self.tr("Please enter a column name."))

	def insert_column_row(self, column_name: str):
		row_pos = self.ui.tableWidget.rowCount()
		self.ui.tableWidget.insertRow(row_pos)
		self.ui.tableWidget.setItem(row_pos, 0, QTableWidgetItem(column_name))

		delete_button = QPushButton()
		delete_button.setIcon(QIcon(":/icons/icons/editbin.svg"))
		apply_icon_button_style(delete_button)
		delete_button.setIconSize(QSize(20, 20))
		delete_button.setFixedSize(24, 24)
		delete_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		delete_button.clicked.connect(lambda: self.ui.tableWidget.removeRow(row_pos))
		self.ui.tableWidget.setCellWidget(row_pos, 1, delete_button)

	def confirm_and_close(self):
		self.selected_columns = []
		for row in range(self.ui.tableWidget.rowCount()):
			item = self.ui.tableWidget.item(row, 0)
			if item:
				self.selected_columns.append(item.text().strip())
		self.accept()






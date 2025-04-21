import fnmatch
from datetime import datetime

from PySide6.QtCore import QDate
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMessageBox, QComboBox, QLineEdit, QDateEdit
from frontend.keystatus import ActivationStatus


class TableOperator:
	r"""
	Class to handle operations on the table, such as adding or deleting rows, filtering rows based on different criteria,
	and handling checkbox selection (check all/uncheck all).
	This class only make UI-level changes.
	"""

	def __init__(self, table_widget):
		r"""
		Initialize the TableOperator with the table widget.

		\param table_widget (QTableWidget): The table widget to operate on.
		"""
		self.table_widget = table_widget

	def add_new_row(self):
		r"""
		Add a new row to the table widget.
		"""
		row_position = self.table_widget.rowCount()
		self.table_widget.insertRow(row_position)

	def delete_row(self):
		r"""
		Delete the currently selected row from the table widget.
		"""
		selected_row = self.table_widget.currentRow()
		if selected_row != -1:
			self.table_widget.removeRow(selected_row)
		else:
			QMessageBox.warning(None, "Warning", "Please select a line first")

	def check_all_boxes(self):
		r"""
		Check or uncheck all checkboxes in the first column of the table. If all boxes are checked, it unchecks them,
		otherwise, it checks all of them.
		"""
		all_checked = True

		for row in range(self.table_widget.rowCount()):
			if not self.table_widget.isRowHidden(row):
				checkbox = self.table_widget.item(row, 0)
				if checkbox is not None:
					if checkbox.checkState() != Qt.CheckState.Checked:
						all_checked = False
						break

		new_state = Qt.CheckState.Unchecked if all_checked else Qt.CheckState.Checked

		for row in range(self.table_widget.rowCount()):
			if not self.table_widget.isRowHidden(row):
				checkbox = self.table_widget.item(row, 0)
				if checkbox is not None:
					checkbox.setCheckState(new_state)

	def filter_table(self, filter_inputs):
		r"""
		Filter the table rows based on user input from various filter fields.
		Rows that do not match the criteria will be hidden.

		\param filter_inputs (dict[str, QWidget]): A dictionary mapping filter label text (also the table column header) to the corresponding input widget (QLineEdit or QComboBox).
		"""

		label_to_index = {}
		for i in range(self.table_widget.columnCount()):
			header_item = self.table_widget.horizontalHeaderItem(i)
			if header_item:
				internal_key = header_item.data(Qt.ItemDataRole.UserRole)
				if internal_key:
					label_to_index[internal_key] = i
				else:
					label_to_index[header_item.text()] = i

		for row in range(self.table_widget.rowCount()):
			match = True

			for label_text, widget in filter_inputs.items():
				if label_text in ["start", "end"]:
					continue

				if label_text in label_to_index:
					col_index = label_to_index[label_text]
				else:
					match = False
					break

				item = self.table_widget.item(row, col_index)
				if item is None:
					match = False
					break

				filter_text = widget.currentText() if isinstance(widget, QComboBox) else widget.text().strip()

				if not filter_text or filter_text == "All" or filter_text == "Alle":
					continue

				if label_text == "status":
					status_value = item.data(Qt.ItemDataRole.UserRole + 1)

					status_mapping = {
						"Activated": ActivationStatus.ACTIVATED,
						"Deactivated": ActivationStatus.DEACTIVATED,
						"Aktiviert": ActivationStatus.ACTIVATED,
						"Deaktiviert": ActivationStatus.DEACTIVATED
					}

					expected_status = status_mapping.get(filter_text, None)

					if expected_status is None or status_value != expected_status:
						match = False
				else:
					if not fnmatch.fnmatch(item.text(), filter_text):
						match = False

			start_widget = filter_inputs.get("start")
			end_widget = filter_inputs.get("end")

			start_date = start_widget.date() if start_widget else None
			end_date = end_widget.date() if end_widget else None
			col_index = label_to_index["last_edit_date"]
			item = self.table_widget.item(row, col_index)
			if item and item.text():
				cell_date = datetime.strptime(item.text(), "%Y-%m-%d").date()

				if start_date and cell_date < start_date:
					match = False
				if end_date and cell_date > end_date:
					match = False
			else:
				match = False

			self.table_widget.setRowHidden(row, not match)

	def reset_filter(self, filter_inputs):
		r"""
		Reset the filters by clearing all input fields and showing all rows in the table

		\param filter_inputs (dict[str, QWidget]): A dictionary mapping filter label text (also the table column header) to the corresponding input widget (QLineEdit or QComboBox).
		"""
		for label_text, widget in filter_inputs.items():
			if isinstance(widget, QLineEdit):
				widget.clear()
			elif isinstance(widget, QComboBox):
				widget.setCurrentIndex(0)
			elif isinstance(widget, QDateEdit):
				if label_text == "Start":
					widget.setDate(QDate(2000, 1, 1))
				elif label_text == "End":
					widget.setDate(QDate.currentDate())
		for row in range(self.table_widget.rowCount()):
			self.table_widget.setRowHidden(row, False)

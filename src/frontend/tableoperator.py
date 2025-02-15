from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMessageBox
from frontend.keystatus import ActivationStatus


class TableOperator:
	r"""
	Class to handle operations on the table, such as adding or deleting rows, filtering rows based on different criteria,
	and handling checkbox selection (check all/uncheck all).
	This class only make UI-level changes without modifying the database.
	"""

	def __init__(self, table_widget):
		r"""
		Initialize the TableOperator with the table widget.

		\param table_widget (QTableWidget): The table widget to operate on.
		"""
		self.table_widget = table_widget

	def add_new_row(self):
		r"""
		Add a new row to the table widget. This function only modifies the UI and does not affect the database.
		"""
		row_position = self.table_widget.rowCount()
		self.table_widget.insertRow(row_position)

	def delete_row(self):
		r"""
		Delete the currently selected row from the table widget.
		This function only modifies the UI and does not affect the database.
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
			if not self.table_widget.isRowHidden(row):  # Only for visible rows (filter)
				checkbox = self.table_widget.item(row, 0)
				if checkbox is not None:
					if checkbox.checkState() != Qt.Checked:
						all_checked = False
						break

		new_state = Qt.Unchecked if all_checked else Qt.Checked

		for row in range(self.table_widget.rowCount()):
			if not self.table_widget.isRowHidden(row):
				checkbox = self.table_widget.item(row, 0)
				if checkbox is not None:
					checkbox.setCheckState(new_state)

	def filter_table(self, serial_number_line_edit, name_line_edit, project_line_edit, operator_line_edit,
					 specimen_line_edit, dfos_type_line_edit, keyfile_line_edit, state_combobox):
		r"""
		Filter the table rows based on user input from various filter fields (serial number, name, project, etc.).
		Rows that do not match the criteria will be hidden.

		\param serial_number_line_edit (QLineEdit): Input field for filtering by serial number.
		\param name_line_edit (QLineEdit): Input field for filtering by sensor name.
		\param project_line_edit (QLineEdit): Input field for filtering by project.
		\param operator_line_edit (QLineEdit): Input field for filtering by operator.
		\param specimen_line_edit (QLineEdit): Input field for filtering by specimen.
		\param dfos_type_line_edit (QLineEdit): Input field for filtering by DFOS type.
		\param keyfile_line_edit (QLineEdit): Input field for filtering by keyfile.
		\param state_combobox (QComboBox): Dropdown for filtering by status ('Activated', 'Deactivated', 'Unknown').
		"""

		serial_number = serial_number_line_edit.text()
		name = name_line_edit.text()
		project = project_line_edit.text()
		operator = operator_line_edit.text()
		specimen = specimen_line_edit.text()
		dfos_type = dfos_type_line_edit.text()
		keyfile = keyfile_line_edit.text()
		state = state_combobox.currentText()

		for row in range(self.table_widget.rowCount()):
			match = True

			serial_item = self.table_widget.item(row, 2)
			name_item = self.table_widget.item(row, 3)
			project_item = self.table_widget.item(row, 4)
			operator_item = self.table_widget.item(row, 5)
			specimen_item = self.table_widget.item(row, 6)
			dfos_type_item = self.table_widget.item(row, 7)
			keyfile_item = self.table_widget.item(row, 10)
			state_item = self.table_widget.item(row, 1)

			if serial_number and serial_number not in serial_item.text():
				match = False
			if name and name not in name_item.text():
				match = False
			if project and project not in project_item.text():
				match = False
			if operator and operator not in operator_item.text():
				match = False
			if specimen and specimen not in specimen_item.text():
				match = False
			if dfos_type and dfos_type not in dfos_type_item.text():
				match = False
			if keyfile and keyfile not in keyfile_item.data(Qt.UserRole + 2):
				match = False
			if state and state != "All":
				if state == 'Activated' and state_item.data(Qt.UserRole + 1) != ActivationStatus.ACTIVATED:
					match = False
				elif state == 'Deactivated' and state_item.data(Qt.UserRole + 1) != ActivationStatus.DEACTIVATED:
					match = False
				elif state == 'Unknown' and state_item.data(Qt.UserRole + 1) != ActivationStatus.UNKNOWN:
					match = False

			# hide rows that do not match the filter criteria
			self.table_widget.setRowHidden(row, not match)

	def reset_filter(self, serial_number_line_edit, name_line_edit, project_line_edit, operator_line_edit,
					 specimen_line_edit, dfos_type_line_edit, keyfile_line_edit):
		r"""
		Reset the filters by clearing all input fields and showing all rows in the table.

		\param serial_number_line_edit (QLineEdit): Input field for filtering by serial number.
		\param name_line_edit (QLineEdit): Input field for filtering by name.
		\param project_line_edit (QLineEdit): Input field for filtering by project.
		\param operator_line_edit (QLineEdit): Input field for filtering by operator.
		\param specimen_line_edit (QLineEdit): Input field for filtering by specimen.
		\param dfos_type_line_edit (QLineEdit): Input field for filtering by DFOS type.
		\param keyfile_line_edit (QLineEdit): Input field for filtering by keyfile.
		"""

		serial_number_line_edit.clear()
		name_line_edit.clear()
		project_line_edit.clear()
		operator_line_edit.clear()
		specimen_line_edit.clear()
		dfos_type_line_edit.clear()
		keyfile_line_edit.clear()

		for row in range(self.table_widget.rowCount()):
			self.table_widget.setRowHidden(row, False)

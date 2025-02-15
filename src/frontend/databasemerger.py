from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from frontend.keyfilecompare import KeyfileCompare
from frontend.ui.uimerge import Ui_Merge


class DatabaseMerger(QDialog):
	r"""
	A dialog window for handle conflict in import external database to current database.
	"""
	def __init__(self, db_handler, conflict_records, parent=None):
		r"""
		Initialize the DatabaseMerger dialog.

		\param db_handler (DatabaseHandler): The database handler to manage and update the current database.
		\param conflict_records (list): A list of tuples representing conflicting records between the existing and imported databases.
		\param parent (optional): The parent widget for this dialog.
		"""
		super().__init__(parent)
		self.db_handler = db_handler
		self.conflict_records = conflict_records
		self.current_conflict_index = 0
		self.imported_keyfile_blob = None

		self.merge_ui = Ui_Merge()
		self.merge_ui.setupUi(self)
		self.resize(1400, 300)

		self.load_conflict_record(self.conflict_records[self.current_conflict_index])

		self.merge_ui.compareKeyfileButton.clicked.connect(self.compare_keyfile_dialog)
		self.merge_ui.currentButton.clicked.connect(self.keep_current_version)
		self.merge_ui.importButton.clicked.connect(self.keep_imported_version)
		self.merge_ui.proceedButton.clicked.connect(self.save_merged_record)
		self.merge_ui.skipButton.clicked.connect(self.next_merge_entry)
		self.merge_ui.finishButton.clicked.connect(self.close_dialog)

		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

	def load_conflict_record(self, conflict_record):
		r"""
		Load a specific conflict record into the UI for display.

		\param conflict_record (tuple): A tuple containing the existing and imported conflicting records.
		"""
		existing_record, imported_record = conflict_record
		keyfile_conflict = existing_record[-1] != imported_record[-1]
		self.imported_keyfile_blob = imported_record[-1]

		self.merge_ui.currentSerialLineEdit.setText(existing_record[0])
		self.merge_ui.currentSerialLineEdit.setReadOnly(True)
		self.merge_ui.importedSerialLineEdit.setText(imported_record[0])
		self.merge_ui.importedSerialLineEdit.setReadOnly(True)

		self.merge_ui.currentNameLineEdit.setText(existing_record[1])
		self.merge_ui.currentNameLineEdit.setReadOnly(True)
		self.merge_ui.importedNameLineEdit.setText(imported_record[1])
		self.merge_ui.importedNameLineEdit.setReadOnly(True)

		self.merge_ui.currentProjectLineEdit.setText(existing_record[2])
		self.merge_ui.currentProjectLineEdit.setReadOnly(True)
		self.merge_ui.importedProjectLineEdit.setText(imported_record[2])
		self.merge_ui.importedProjectLineEdit.setReadOnly(True)

		self.merge_ui.currentOperatorLineEdit.setText(existing_record[3])
		self.merge_ui.currentOperatorLineEdit.setReadOnly(True)
		self.merge_ui.importedOperatorLineEdit.setText(imported_record[3])
		self.merge_ui.importedOperatorLineEdit.setReadOnly(True)

		self.merge_ui.currentSpecimenLineEdit.setText(existing_record[4])
		self.merge_ui.currentSpecimenLineEdit.setReadOnly(True)
		self.merge_ui.importedSpecimenLineEdit.setText(imported_record[4])
		self.merge_ui.importedSpecimenLineEdit.setReadOnly(True)

		self.merge_ui.currentTypeLineEdit.setText(existing_record[5])
		self.merge_ui.currentTypeLineEdit.setReadOnly(True)
		self.merge_ui.importedTypeLineEdit.setText(imported_record[5])
		self.merge_ui.importedTypeLineEdit.setReadOnly(True)

		self.merge_ui.currentInstallLineEdit.setText(existing_record[6])
		self.merge_ui.currentInstallLineEdit.setReadOnly(True)
		self.merge_ui.importedInstallLineEdit.setText(imported_record[6])
		self.merge_ui.importedInstallLineEdit.setReadOnly(True)

		self.merge_ui.currentNotelineEdit.setText(existing_record[7])
		self.merge_ui.currentNotelineEdit.setReadOnly(True)
		self.merge_ui.importedNoteLineEdit.setText(imported_record[7])
		self.merge_ui.importedNoteLineEdit.setReadOnly(True)

		self.merge_ui.mergedSerialLineEdit.setText(existing_record[0])
		self.merge_ui.mergedNameLineEdit.setText(self.get_merged_value(existing_record[1], imported_record[1]))
		self.merge_ui.mergedProjectLineEdit.setText(self.get_merged_value(existing_record[2], imported_record[2]))
		self.merge_ui.mergedOperatorLineEdit.setText(self.get_merged_value(existing_record[3], imported_record[3]))
		self.merge_ui.mergedSpecimenLineEdit.setText(self.get_merged_value(existing_record[4], imported_record[4]))
		self.merge_ui.mergedTypeLineEdit.setText(self.get_merged_value(existing_record[5], imported_record[5]))
		self.merge_ui.mergedInstallLineEdit.setText(self.get_merged_value(existing_record[6], imported_record[6]))
		self.merge_ui.mergedNoteLineEdit.setText(self.get_merged_value(existing_record[7], imported_record[7]))

		self.merge_ui.compareKeyfileButton.setEnabled(keyfile_conflict)

		if keyfile_conflict:
			self.merge_ui.currentRadioButton.setEnabled(True)
			self.merge_ui.importedRadioButton.setEnabled(True)
			self.merge_ui.currentRadioButton.setChecked(True)
		else:
			self.merge_ui.currentRadioButton.setEnabled(False)
			self.merge_ui.importedRadioButton.setEnabled(False)

	def get_merged_value(self, current_value, imported_value):
		r"""
		Determine the merged value based on the current and imported values.

		\param current_value (str): The value from the current record.
		\param imported_value (str): The value from the imported record.
		\return (str): The merged value, combining or prioritizing based on the input values.
		"""
		if current_value and imported_value:
			if current_value == imported_value:
				return current_value
			else:
				return f"{current_value} {imported_value}"
		elif current_value:
			return current_value
		elif imported_value:
			return imported_value
		else:
			return ""

	def compare_keyfile_dialog(self):
		r"""Open a dialog for the user to compare the contents of conflicting keyfile versions.	"""
		conflict_record = self.conflict_records[self.current_conflict_index]
		current_keyfile_blob = conflict_record[0][-1]
		imported_keyfile_blob = conflict_record[1][-1]

		dialog = KeyfileCompare(current_keyfile_blob, imported_keyfile_blob, self)
		dialog.exec_()

	def keep_current_version(self):
		r"""Copy all information from the current record fields to the merged record fields."""
		self.merge_ui.mergedSerialLineEdit.setText(self.merge_ui.currentSerialLineEdit.text())
		self.merge_ui.mergedNameLineEdit.setText(self.merge_ui.currentNameLineEdit.text())
		self.merge_ui.mergedProjectLineEdit.setText(self.merge_ui.currentProjectLineEdit.text())
		self.merge_ui.mergedOperatorLineEdit.setText(self.merge_ui.currentOperatorLineEdit.text())
		self.merge_ui.mergedSpecimenLineEdit.setText(self.merge_ui.currentSpecimenLineEdit.text())
		self.merge_ui.mergedTypeLineEdit.setText(self.merge_ui.currentTypeLineEdit.text())
		self.merge_ui.mergedInstallLineEdit.setText(self.merge_ui.currentInstallLineEdit.text())
		self.merge_ui.mergedNoteLineEdit.setText(self.merge_ui.currentNotelineEdit.text())

	def keep_imported_version(self):
		r"""Copy all information from the imported record fields to the merged record fields."""
		self.merge_ui.mergedSerialLineEdit.setText(self.merge_ui.importedSerialLineEdit.text())
		self.merge_ui.mergedNameLineEdit.setText(self.merge_ui.importedNameLineEdit.text())
		self.merge_ui.mergedProjectLineEdit.setText(self.merge_ui.importedProjectLineEdit.text())
		self.merge_ui.mergedOperatorLineEdit.setText(self.merge_ui.importedOperatorLineEdit.text())
		self.merge_ui.mergedSpecimenLineEdit.setText(self.merge_ui.importedSpecimenLineEdit.text())
		self.merge_ui.mergedTypeLineEdit.setText(self.merge_ui.importedTypeLineEdit.text())
		self.merge_ui.mergedInstallLineEdit.setText(self.merge_ui.importedInstallLineEdit.text())
		self.merge_ui.mergedNoteLineEdit.setText(self.merge_ui.importedNoteLineEdit.text())

	def save_merged_record(self):
		r"""
		Check if the current merge result is valid, and if so, save it.
		If there is a conflict in the keyfile, update the data blob file based on the chosen version.
		"""

		if not self.is_merge_valid():
			return

		row_data = [
			self.merge_ui.mergedSerialLineEdit.text(),
			self.merge_ui.mergedNameLineEdit.text(),
			self.merge_ui.mergedProjectLineEdit.text(),
			self.merge_ui.mergedOperatorLineEdit.text(),
			self.merge_ui.mergedSpecimenLineEdit.text(),
			self.merge_ui.mergedTypeLineEdit.text(),
			self.merge_ui.mergedInstallLineEdit.text(),
			self.merge_ui.mergedNoteLineEdit.text()
		]

		self.db_handler.update_data(row_data)

		serial_number = row_data[0]

		if self.merge_ui.importedRadioButton.isEnabled() and self.merge_ui.importedRadioButton.isChecked():
			self.db_handler.update_blob_data(self.imported_keyfile_blob, serial_number)

		self.db_handler.connection.commit()

		if self.current_conflict_index == len(self.conflict_records) - 1:
			self.accept()

		self.next_merge_entry()

	def next_merge_entry(self):
		r"""
		Proceed to the next conflict record. If this is the last conflict record, disable the "Next" button.
		"""
		if self.current_conflict_index >= len(self.conflict_records) - 1:
			self.accept()
			return

		self.current_conflict_index += 1
		self.load_conflict_record(self.conflict_records[self.current_conflict_index])

		if self.current_conflict_index == len(self.conflict_records) - 1:
			self.merge_ui.skipButton.setDisabled(True)

	def is_merge_valid(self):
		r"""
		Check if the merged content is valid.
		Validation criteria:
		- The Serial Number (primary key) must be filled.
		- The Serial Number must match the current and imported entries.

		\return (bool): True if the merge is valid, otherwise False.
		"""
		merged_serial = self.merge_ui.mergedSerialLineEdit.text().strip()
		current_serial = self.merge_ui.currentSerialLineEdit.text().strip()
		imported_serial = self.merge_ui.importedSerialLineEdit.text().strip()

		if not (merged_serial and (merged_serial == current_serial or merged_serial == imported_serial)):
			self.merge_ui.mergedSerialLineEdit.setStyleSheet("border: 2px solid red;")
			return False
		else:
			self.merge_ui.mergedSerialLineEdit.setStyleSheet("")

		return True

	def close_dialog(self):
		r"""Close the current dialog window."""
		self.close()

from PySide6.QtCore import Qt
from frontend.keystatus import DBStatus, ActivationStatus


class ToolManager:
	r"""
	Manage the toolbar actions in the UI, enabling or disabling them based on the current selection
	and status of the table rows.

	The ToolManager is responsible for managing actions like creating new entries, deleting rows,
	saving changes, importing key files, attaching key files, replacing mismatched key files,
	and copying key files. It dynamically updates the status of these actions based on the status of  selected table item.
	"""

	def __init__(self, table_widget, action_new, action_delete, action_save_change,
				action_import, action_attach, action_replace, action_copy):
		r"""
		Initialize the ToolManager with the table widget and all relevant actions.

		\param table_widget (QTableWidget): The table widget to track for item selection changes.
		\param action_new (QAction): The action for creating a new entry.
		\param action_delete (QAction): The action for deleting an entry.
		\param action_save_change (QAction): The action for saving changes.
		\param action_import (QAction): The action for importing a keyfile.
		\param action_attach (QAction): The action for attaching a keyfile.
		\param action_replace (QAction): The action for replacing a mismatched keyfile.
		\param action_copy (QAction): The action for copying a keyfile.
		"""
		self.table_widget = table_widget

		self.action_new = action_new
		self.action_delete = action_delete
		self.action_save_change = action_save_change
		self.action_import = action_import
		self.action_attach = action_attach
		self.action_replace = action_replace
		self.action_copy = action_copy

		self.disable_all_actions()

		self.table_widget.itemSelectionChanged.connect(self.update_action_status)

	def disable_all_actions(self):
		r"""
		Disable all toolbar actions, except for the save action which remains enabled.
		This is used to reset the toolbar actions when no row is selected or there is no valid selection.
		"""
		self.action_new.setEnabled(False)
		self.action_delete.setEnabled(False)
		self.action_save_change.setEnabled(True)
		self.action_import.setEnabled(False)
		self.action_attach.setEnabled(False)
		self.action_replace.setEnabled(False)
		self.action_copy.setEnabled(False)

	def update_action_status(self):
		r"""
		Update the status of toolbar actions based on the currently selected row in the table.

		Depending on the database status of the selected row (e.g., EXISTS, MISSING_KEYFILE, NOT_EXISTS, MISMATCH),
		different actions will be enabled or disabled. If no valid row is selected, all actions will be disabled.
		"""

		selected_items = self.table_widget.selectedItems()

		if not selected_items:
			self.disable_all_actions()
			return

		selected_item = selected_items[0]
		row = selected_item.row()
		icon_item = self.table_widget.item(row, 10)
		if icon_item is None:
			self.disable_all_actions()
			return

		status = icon_item.data(Qt.UserRole)

		if status == DBStatus.EXISTS:
			self.action_new.setEnabled(True)
			self.action_delete.setEnabled(True)
			self.action_save_change.setEnabled(True)
			self.action_import.setEnabled(False)
			self.action_attach.setEnabled(False)

			activation_item = self.table_widget.item(row, 1)
			if activation_item is not None:
				activation_status = activation_item.data(Qt.UserRole + 1)
				if activation_status == ActivationStatus.UNKNOWN:
					self.action_copy.setEnabled(True)
				else:
					self.action_copy.setEnabled(False)
			else:
				self.action_copy.setEnabled(False)
			self.action_replace.setEnabled(False)

		elif status == DBStatus.MISSING_KEYFILE:
			self.action_new.setEnabled(True)
			self.action_delete.setEnabled(True)
			self.action_save_change.setEnabled(True)
			self.action_import.setEnabled(False)
			self.action_attach.setEnabled(True)
			self.action_copy.setEnabled(False)
			self.action_replace.setEnabled(False)

		elif status == DBStatus.NOT_EXISTS:
			self.action_new.setEnabled(False)
			self.action_delete.setEnabled(False)
			self.action_save_change.setEnabled(True)
			self.action_import.setEnabled(True)
			self.action_attach.setEnabled(False)
			self.action_copy.setEnabled(False)
			self.action_replace.setEnabled(False)

		elif status == DBStatus.MISMATCH:
			self.action_new.setEnabled(True)
			self.action_delete.setEnabled(True)
			self.action_save_change.setEnabled(True)
			self.action_import.setEnabled(False)
			self.action_attach.setEnabled(False)
			self.action_copy.setEnabled(False)
			self.action_replace.setEnabled(True)

		else:
			self.disable_all_actions()

from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QEvent, QTimer, QPoint
from frontend.keystatus import DBStatus, ActivationStatus


class HoverInfo(QDialog):
	r"""
	A tooltip dialog that provides detailed information about a table cell when the mouse hovers over it.

	This class creates a small hover window that displays information such as the cell's content,
	the activation status of the keyfile, and its status in the database. It is triggered when the mouse
	hovers over a cell in the associated table widget.
	"""
	def __init__(self, table_widget, parent=None):
		r"""
		Initialize the HoverInfo dialog with the table widget to monitor.

		\param table_widget (QTableWidget): The table widget to track mouse hover events on.
		\param parent (QWidget, optional): The parent widget.
		"""

		super(HoverInfo, self).__init__(parent)

		self.setWindowFlags(Qt.ToolTip)
		layout = QVBoxLayout()

		self.cell_label = QLabel(self.tr("Cell: "))
		layout.addWidget(self.cell_label)

		self.activate_label = QLabel(self.tr("Activation Status: "))
		layout.addWidget(self.activate_label)

		self.db_status_label = QLabel(self.tr("Database Status: "))
		layout.addWidget(self.db_status_label)

		self.setLayout(layout)

		# Initialize a timer for delayed tooltip display
		self.timer = QTimer(self)
		self.timer_signal_connected = False

		# Associated table widget to track mouse movements
		self.table_widget = table_widget
		self.table_widget.setMouseTracking(True)
		self.table_widget.viewport().installEventFilter(self)

	def eventFilter(self, source, event):
		r"""
		Capture mouse hover events and display hover info.

		This method handles mouse movement over the table widget to determine which cell the mouse is over,
		and then triggers the tooltip display after a delay.

		\param source (QObject): The source widget that the event is coming from (table widget viewport).
		\param event (QEvent): The event being processed (mouse movement).
		\return (bool): Returns True if the event is handled, otherwise False to pass the event to the base class.
		"""
		if event.type() == QEvent.MouseMove:
			if source == self.table_widget.viewport():
				pos = event.pos()
				item = self.table_widget.itemAt(pos)
				if item:
					column = item.column()
					if column >= 2:
						if self.timer_signal_connected:
							self.timer.timeout.disconnect()
							self.timer_signal_connected = False

						# Connect the timer's timeout signal to display hover info after a delay
						self.timer.timeout.connect(lambda: self.show_hover_info(item, pos))
						self.timer_signal_connected = True
						self.timer.start(1000)
					else:
						if self.isVisible():
							self.hide()
						self.timer.stop()

		elif event.type() == QEvent.Leave:
			if self.isVisible():
				self.hide()
			self.timer.stop()

		return super().eventFilter(source, event)

	def show_hover_info(self, item, pos):
		r"""
		Show the hover info dialog with details about the cell.
		Hover info includes the table header name of this column, cell value, activation status,
		and database status.

		\param item (QTableWidgetItem): The table cell item that is being hovered over.
		\param pos (QPoint): The current position of the mouse cursor.
		"""
		row = item.row()
		col = item.column()

		column_name = self.table_widget.horizontalHeaderItem(col).text()
		if col == 10:
			cell_value = item.data(Qt.UserRole + 2)
		else:
			cell_value = item.text()

		activation_item = self.table_widget.item(row, 1)
		if activation_item:
			activation_status = activation_item.data(Qt.UserRole + 1)
			if activation_status == ActivationStatus.ACTIVATED:
				activate_status = self.tr("Keyfile is Activated")
			elif activation_status == ActivationStatus.DEACTIVATED:
				activate_status = self.tr("Keyfile is Deactivated")
			elif activation_status == ActivationStatus.UNKNOWN:
				activate_status = self.tr("Keyfile Missing in Disk")
			else:
				activate_status = self.tr("Unknown")
		else:
			activate_status = self.tr("Unknown")

		icon_column_item = self.table_widget.item(row, 10)
		if icon_column_item:
			status = icon_column_item.data(Qt.UserRole)
			if status == DBStatus.EXISTS:
				db_status = self.tr("Exists in Database")
			elif status == DBStatus.MISSING_KEYFILE:
				db_status = self.tr("Keyfile Missing in Database")
			elif status == DBStatus.NOT_EXISTS:
				db_status = self.tr("Not Exists in Database")
			elif status == DBStatus.MISMATCH:
				db_status = self.tr("Keyfile Mismatch between database and disk")
			else:
				db_status = self.tr("Unknown")
		else:
			db_status = self.tr("Unknown")

		# self.cell_label.setText(f"{column_name}: {cell_value}")
		# self.activate_label.setText(f"Activation Status: {activate_status}")
		# self.db_status_label.setText(f"Database Status: {db_status}")

		self.cell_label.setText(f"{column_name}: {cell_value}")
		self.activate_label.setText(
			self.tr("Activation Status: {activate_status}").format(activate_status=activate_status))
		self.db_status_label.setText(self.tr("Database Status: {db_status}").format(db_status=db_status))

		table_pos = self.table_widget.mapToGlobal(pos)
		self.move(table_pos + QPoint(20, 80))  # show in bottom right corner of the mouse
		self.show()


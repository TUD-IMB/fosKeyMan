from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from frontend.ui.uirename import Ui_Rename


class RenameSensor(QDialog):
	r"""
	Dialog to rename the sensor name.
	"""
	def __init__(self, serial_number, sensor_name, parent=None):
		r"""
		Initialize the RenameSensor dialog.

		\param serial_number (str): The serial number of the sensor.
		\param sensor_name (str): The current name of the sensor.
		\param parent (QWidget, optional): The parent widget for this dialog.
		"""
		super(RenameSensor, self).__init__(parent)

		self.serial_number = serial_number
		self.sensor_name = sensor_name

		self.rename_ui = Ui_Rename()
		self.rename_ui.setupUi(self)

		self.rename_ui.serialNumberLabel2.setText(self.serial_number)
		self.rename_ui.sensorNameLineEdit.setText(self.sensor_name)

		self.rename_ui.renameButton.clicked.connect(self.rename)
		self.rename_ui.cancelButton.clicked.connect(self.reject)

		self.new_name = None

		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

	def rename(self):
		r"""Get the new name from the QLineEdit and accept the dialog."""
		self.new_name = self.rename_ui.sensorNameLineEdit.text()
		self.accept()

	def get_new_sensor_name(self):
		r"""
		Retrieve the new sensor name.

		\return (str): The new sensor name.
		"""
		return getattr(self, 'new_name', self.sensor_name)

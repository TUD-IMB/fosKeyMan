from enum import Enum


class ActivationStatus(Enum):
	r"""
	Enumeration to represent the activation status of a keyfile.
	- ACTIVATED: The keyfile is activated and exist on the disk.
	- DEACTIVATED: The keyfile is deactivated and exist on the disk.
	- UNKNOWN: The keyfile is found neither in the activated nor the deactivated directory.
	"""
	ACTIVATED = 1
	DEACTIVATED = 2
	UNKNOWN = 3

from enum import Enum


class DBStatus(Enum):
	r"""
	Enumeration to represent the different statuses of a keyfile in the database.
	- EXISTS: The keyfile exists in the database.
	- MISSING_KEYFILE: The keyfile's record exists in the database, but the keyfile itself is missing.
	- NOT_EXISTS: The keyfile does not exist in the database.
	- MISMATCH: There is a mismatch between the keyfile in the database and the one on the disk.
	"""

	EXISTS = 1
	MISSING_KEYFILE = 2
	NOT_EXISTS = 3
	MISMATCH = 4


class ActivationStatus(Enum):
	r"""
	Enumeration to represent the activation status of a keyfile.
	- ACTIVATED: The keyfile is activated and exist on the disk.
	- DEACTIVATED: The keyfile is deactivated and exist on the disk.
	- UNKNOWN: The keyfile is found neither in the activated nor the deactivated directory. (2 types)
		- In the database: The file is found in the database, but not in the directories.
		- Missing: The file is found neither in the directories nor in the database.
	"""
	ACTIVATED = 1
	DEACTIVATED = 2
	UNKNOWN = 3


"""
Script to typeset the database columns as markdown table (used in README).

\author Bertram Richter
\date 2024-08-07
"""

import brplotviz

database_table = [
	["Column Name", "Data Type", "Description"],
	["serial_number", "str", "Serial number of the senosr, used as primary key in the database"],
	["name", "str", "Human readable name of the DFOS"],
	["project", "str", "Project in which the DFOS is used"],
	["operator", "str", "Person responsible for the DFOS"],
	["specimen", "str", "Name of the specimen which the DFOS is attached to"],
	["dfos_type", "str", "Type of the cable itself (coating material, diameter, etc)"],
	["installation","str", "How the DFOS is installed at/in the specimen"],
	["status", "str", "State of the sensor (intact, defect, disposed, ...)"],
	["notes", "str", "Verbose description of the sensor and its use"],
	["keyfile", "binary", "The ODiSI key file as attachment"],
	["...", "...", "Optionally more data (to be continued)"],
	]

key_state_table = [
	["Activation", "Serial number in data base", "File attached", "Activation", "Optional actions"],
	["activated", "no", "no", "deactivate (move file)", "import (add key serial number and metadata and attach file)"],
	["deactivated", "no", "no", "activate (move file)", "import (add key serial number and metadata and attach file)"],
	
	["activated", "yes", "no", "deactivate (move file)", "attach file"],
	["deactivated", "yes", "no", "activate (move file)", "attach file"],
	
	["activated", "yes", "yes", "deactivate (move file)", "check file for identity: replace in database or on disk"],
	["deactivated", "yes", "yes", "activate (move file)", "check file for identity: replace in database or on disk"],
	
	["unknown", "yes", "no", "file is missing!", "warn"],
	["unknown", "yes", "yes", "activate (copy key file to disk)"],
	]

brplotviz.table.print_table(database_table, style="markdown", style_kwargs={"pad_left": " ", "pad_right": " "})
print()
brplotviz.table.print_table(key_state_table, style="markdown", style_kwargs={"pad_left": " ", "pad_right": " "})

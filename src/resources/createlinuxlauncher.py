
r"""
Create a Linux launcher file for fosKeyMan.
It is assumed, that the current directory:
- contains the binary (compiled program) called `fosKeyMan`,
- contains the logo `foskeyman_logo_short.svg`.
- will be the working directory for `fosKeyMan` (config and log files will be written here).

The file `fosKeyMan.desktop` is created in the current directory.
The file can be copied to the desktop.
Copy the launcher to `~/.local/share/applications/` if you want the
launcher to show up in the start menu of the desktop environment

For the documentation on the format, see the
[Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/).

\author Bertram Richter
\date 2025
"""

import os

filecontent = \
r"""
[Desktop Entry]
Type =		Application
Name =		fosKeyMan
Comment =	Fiber optic Sensor Key Manager
Icon =		{iconpath}
Categories =	Office;Utility;Settings
Path = {directory}
Terminal =	false
Exec =		{binpath}
"""

def main():
	r"""
	"""
	directory = os.getcwd()
	iconpath = os.path.join(directory, "foskeyman_logo_short.svg")
	binpath = os.path.join(directory, "fosKeyMan")
	filecontent_filled = filecontent.format(
		iconpath=iconpath,
		directory=directory,
		binpath=binpath,
		)
	with open(os.path.join(directory, "fosKeyMan.desktop"), "w", encoding="utf-8") as launcher:
		launcher.write(filecontent_filled)

if __name__ == "__main__":
	main()

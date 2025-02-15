
r"""
This script is used to convert the Qt Designer UI files and icons to Python files.
"""

import os
import subprocess
import re

base_dir = os.path.abspath(os.path.dirname(__file__))
ui_source_dir = os.path.join(base_dir, 'resources/ui')
qrc_source_dir = os.path.join(base_dir, 'resources')
py_target_dir = os.path.join(base_dir, 'frontend/ui')


def convert_ui_files():
	r"""
	Convert Qt Designer UI files to Python files.
	"""
	for file_name in os.listdir(ui_source_dir):
		if file_name.endswith('.ui'):
			ui_file_path = os.path.join(ui_source_dir, file_name).replace("\\", "/")
			py_file_name = f"ui{os.path.splitext(file_name)[0]}.py"
			py_file_path = os.path.join(py_target_dir, py_file_name).replace("\\", "/")

			if os.path.exists(ui_file_path):
				command = f'./pyside6-uic "{ui_file_path}" -o "{py_file_path}"'
				try:
					result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					print(f"Successfully converted {ui_file_path} to {py_file_path}.")
					modify_import_statement(py_file_path)
				except subprocess.CalledProcessError as e:
					print(f"Converting {ui_file_path} failed: {e}")
			else:
				print(f"File does not exist: {ui_file_path}")


def modify_import_statement(py_file_path):
	with open(py_file_path, 'r', encoding='utf-8') as file:
		content = file.read()
	# 'import toolicons_rc' -> 'from frontend.ui import toolicons_rc'
	content = re.sub(r'import (\w+_rc)', r'from frontend.ui import \1', content)
	with open(py_file_path, 'w', encoding='utf-8') as file:
		file.write(content)


def convert_qrc_files():
	r"""
	Convert ressource files to Python files.
	"""
	for file_name in os.listdir(qrc_source_dir):
		if file_name.endswith('.qrc'):
			qrc_file_path = os.path.join(qrc_source_dir, file_name)
			py_file_name = f"{os.path.splitext(file_name)[0]}_rc.py"
			py_file_path = os.path.join(py_target_dir, py_file_name).replace("\\", "/")

			if os.path.exists(qrc_file_path):
				command = f'./pyside6-rcc "{qrc_file_path}" -o "{py_file_path}"'
				try:
					result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					print(f"Successfully converted {qrc_file_path} to {py_file_path}")
				except subprocess.CalledProcessError as e:
					print(f"Converting {qrc_file_path} failed: {e}")
			else:
				print(f"The file does not exist:{qrc_file_path}")


if __name__ == '__main__':
	if not os.path.exists(py_target_dir):
		os.makedirs(py_target_dir)
	
	print("Start converting .ui files…")
	convert_ui_files()

	print("\nStart converting .qrc files…")
	convert_qrc_files()


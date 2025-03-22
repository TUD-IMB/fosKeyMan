def format_json_to_html(json_data):
	r"""
	Format JSON data as HTML for display in a QTextBrowser.
	\param json_data: str The JSON data as a formatted string.
	\return: str The HTML-formatted string for displaying in QTextBrowser.
	"""
	html_content = f"""
	<pre style="
		font-family: monospace;
		color: #333;
		background-color: #f9f9f9;
		padding: 10px;
		white-space: pre-wrap;
		word-wrap: break-word;
	">{json_data}</pre>
	"""
	return html_content


def apply_icon_button_style(button):
	button_style = """
	QPushButton {
		border: none;
		background: transparent;
		padding: 2px;
	}
	QPushButton:hover {
		background-color: lightgray;
		border-radius: 4px;
	}
	QPushButton:pressed {
		background-color: lightblue;
		border-radius: 4px;
	}
	"""
	button.setStyleSheet(button_style)

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

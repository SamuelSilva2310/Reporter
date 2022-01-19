class Row:
	def __init__(self, data):
		"""
			data: [cpu,memory...] List with all data 
		"""
		self.data = data
		self.row_marker = None # Indicator for different areas of our file (Ex: database section values, api request values...)
	
	def get_data(self):
		return self.data
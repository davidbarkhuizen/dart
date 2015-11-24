class AnalysisReport(object):

	def __init__(self, symbol, start_date, end_date, description, text, figure):

		self.symbol = symbol
		self.start_date = start_date
		self.end_date = end_date
		self.description = description
		self.text = text
		self.figure = figure
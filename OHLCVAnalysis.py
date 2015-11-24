from histogram import Histogram

class OHLCVAnalysis:

	def __init__(self, dates, open, high, low, close, vol, start, end):
		
		if start > end:
			(start, end) = (end, start)
		
		self.report_log = []    
		
		max = None
		max_date = None
		min = None
		min_date = None
		
		seq_start = dates[0]
		seq_end = dates[0]
		
		series = []
		
		n = 0
	 
		for i in range(len(dates)):    
		 
			d = dates[i]
			if (d > start) and (d < end):      
				
				series.append(close[i])
				
				if (d < seq_start):
					seq_start = d
				if (d > seq_end):
					seq_end = d

				n = n + 1 
				
				h = high[i]
				if max == None:
					max = h
					max_date = d
				else:
					if h > max:
						max = h
						max_date = d
						
				l = low[i]
				if min == None:
					min = l
					min_date = d
				else:
					if l < min:
						min = l
						min_date = d
		
		self.report_log.append('%s - %s' % (seq_start, seq_end))
		self.report_log.append('%d trading days' % n)
		self.report_log.append('Max = %s - %s' % (str(max), max_date))
		self.report_log.append('Min = %s - %s' % (str(min), min_date))
		
		#~ h = Histogram(series)
		#~ for l in h.report():
			#~ self.report_log.append(l)
		
	def report(self):
		return self.report_log

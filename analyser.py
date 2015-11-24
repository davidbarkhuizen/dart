# standard lib
import datetime
import math
# 3rd party libs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# django domain models
from OHLCVAnalysis import OHLCVAnalysis
from histogram import Histogram

class Analysis:
	def __init__(self, name, plot_ref, report):
		self.name = name
		self.plot_ref = plot_ref
		self.report = report

def gen_dual_series_scatter_plot(symbol, dates, values, volume, start_date, end_date, gen_title):
	'''
	extract specified slice from total series, generate and return matplotlib figure for slice
	'''
	# extract desired time-slice from total series  
	if (dates[0] < dates[len(dates) - 1]):
		start_idx = 0
		for i in range(0, len(dates)):
			if dates[i] <= start_date:
				start_idx = i
			else:      
				break
		end_idx = 0
		for i in range(0, len(dates)):
			if dates[i] <= end_date:
				end_idx = i
			else:
				break
	else:
		start_idx = 0
		for i in range(0, len(dates)):
			if dates[i] >= start_date:
				start_idx = i
			else:      
				break
		end_idx = 0
		for i in range(0, len(dates)):
			if dates[i] >= end_date:
				end_idx = i
			else:
				break

	# swap if start_date after end_date
	if (start_idx > end_idx):
		(start_idx, end_idx) = (end_idx, start_idx)

	# if start_date = end_date, use entire series
	if (start_idx == end_idx):
		start_idx = 0
		end_idx = len(dates)
		
	# cut slice
	date_slice = dates[start_idx : end_idx]
	slice_start_date = dates[start_idx]
	slice_end_date = dates[end_idx]
	values_slice = values[start_idx : end_idx]
	volume_slice = volume[start_idx : end_idx]

	# generate matplotlib plot
	x = np.array(date_slice)
	y = np.array(values_slice)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	fig.autofmt_xdate(rotation=90)
	ax.plot(x,y, color='blue')
	# leg = ax.legend(('Model length'), 'upper center', shadow=True)

	# volume plot, same x axis, diff y axis
	v = np.array(volume_slice)
	got_vol_series = False
	if ((volume_slice != None) and (len(v) == len(x))):  
		ax2 = ax.twinx()   
		fig.autofmt_xdate(rotation=90)
		ax2.plot(x, v, color='yellow')
		got_vol_series = True

	ax.grid(False)  
	ax.set_ylabel('Closing Price')

	title = gen_title(symbol, 'Closing Price & Volume Traded', slice_start_date, slice_end_date)
	ax.set_title(title)
	
	fig.autofmt_xdate(rotation=90)
	
	# date intervals & markers
	(formatter, locator) = tick_info(slice_start_date, slice_end_date)
	ax.xaxis.set_major_formatter(formatter) 
	ax.xaxis.set_major_locator(locator)  
	ax.set_xlim([slice_start_date, slice_end_date])
	ax.set_xlabel('Date')  
	
	fig.autofmt_xdate(rotation=90)

	if (got_vol_series):
		#x2.set_xlim([0, np.e]);
		ax2.set_ylabel('Volume Traded');  
		plt.setp(ax2.get_xticklabels(), visible=False)
		plt.setp(ax2.get_xaxis ().get_label().set_visible(False))
	
	#fig.autofmt_xdate(rotation=90)
	#formatter = mpl.dates.DateFormatter(None)
	#locator = mpl.dates.YearLocator(None)
	#ax2.xaxis.set_major_formatter(formatter) 
	#ax2.xaxis.set_major_locator(locator)  
	#fig.autofmt_xdate()   

	return plt

def analyse_daily_open_to_close_movement(symbol, dates, openn, close, start_date, end_date, gen_title) :

	# extract desired time-slice from total series  
	#
	if (dates[0] < dates[len(dates) - 1]):
		start_idx = 0
		for i in range(0, len(dates)):
			if dates[i] <= start_date:
				start_idx = i
			else:      
				break
		end_idx = 0
		for i in range(0, len(dates)):
			if dates[i] <= end_date:
				end_idx = i
			else:
				break
	else:
		start_idx = 0
		for i in range(0, len(dates)):
			if dates[i] >= start_date:
				start_idx = i
			else:      
				break
		end_idx = 0
		for i in range(0, len(dates)):
			if dates[i] >= end_date:
				end_idx = i
			else:
				break

	# swap if start_date after end_date
	if (start_idx > end_idx):
		(start_idx, end_idx) = (end_idx, start_idx)

	# if start_date = end_date, use entire series
	if (start_idx == end_idx):
		start_idx = 0
		end_idx = len(dates)
		
	# cut time slice
	#
	date_slice = dates[start_idx : end_idx]
	slice_start_date = dates[start_idx]
	slice_end_date = dates[end_idx]
	
	open_slice = openn[start_idx : end_idx]
	close_slice = close[start_idx : end_idx]
	
	delta = []
	for i in range(len(open_slice)):
		delta.append(float(100 * (close_slice[i] - open_slice[i]) / close_slice[i]) )
	
	# -------------------------------------
	# % intra-day movement - time series

	# generate matplotlib plot
	#
	x = np.array(date_slice)
	y = np.array(delta)
	fever_fig = plt.figure()
	ax = fever_fig.add_subplot(111)
	ax.plot(x,y)
	# leg = ax.legend(('Model length'), 'upper center', shadow=True)
	
	title = gen_title(symbol, '% (close - open) / open', slice_start_date, slice_end_date)

	ax.grid(False)  
	ax.set_ylabel('100 * (Close - Open) / Open')
	ax.set_title(title)
	# date intervals & markers
	(formatter, locator) = tick_info(slice_start_date, slice_end_date)
	ax.xaxis.set_major_formatter(formatter) 
	ax.xaxis.set_major_locator(locator)
	fever_fig.autofmt_xdate(rotation=90)
	ax.set_xlim([slice_start_date, slice_end_date])
	ax.set_xlabel('Date')
	
	# -------------------------------------
	# % intra-day movement - distribution
	
	h = Histogram(delta)
	left_edge = []
	height = []
	for bin in h.bins:
		left_edge.append(float(bin.floor))
		height.append(h.bin_contrib_perc(bin))
	
	x = np.array(left_edge)
	y = np.array(height)
	
	dist_fig = plt.figure()
	ax = dist_fig.add_subplot(111)
	ax.bar(x, y, width=h.bins[0].range)
	
	ax.set_xlim(h.min, h.max)
	ax.set_ylabel('% of Population')
	ax.set_xlabel('Move i.t.o Open : 100 * (Close - Open) / Open')
	
	title = gen_title(symbol, 'Distribution of Daily Movements', slice_start_date, slice_end_date)
	ax.set_title(title)

	return fever_fig, dist_fig
	
def gen_intraday_volatility_plots(symbol, dates, high, low, close, start_date, end_date, gen_title) :

	# extract desired time-slice from total series  
	#
	if (dates[0] < dates[len(dates) - 1]):
		start_idx = 0
		for i in range(0, len(dates)):
			if dates[i] <= start_date:
				start_idx = i
			else:      
				break
		end_idx = 0
		for i in range(0, len(dates)):
			if dates[i] <= end_date:
				end_idx = i
			else:
				break
	else:
		start_idx = 0
		for i in range(0, len(dates)):
			if dates[i] >= start_date:
				start_idx = i
			else:      
				break
		end_idx = 0
		for i in range(0, len(dates)):
			if dates[i] >= end_date:
				end_idx = i
			else:
				break

	# swap if start_date after end_date
	if (start_idx > end_idx):
		(start_idx, end_idx) = (end_idx, start_idx)

	# if start_date = end_date, use entire series
	if (start_idx == end_idx):
		start_idx = 0
		end_idx = len(dates)
		
	# cut slice
	date_slice = dates[start_idx : end_idx]
	slice_start_date = dates[start_idx]
	slice_end_date = dates[end_idx]
	low_slice = low[start_idx : end_idx]
	high_slice = high[start_idx : end_idx]
	close_slice = close[start_idx : end_idx]
	
	delta = []
	for i in range(len(high_slice)):
		delta.append(float(100 * (high_slice[i] - low_slice[i]) / close_slice[i]) )

	
	# generate matplotlib plot
	x = np.array(date_slice)
	y = np.array(delta)
	fever_fig = plt.figure()
	ax = fever_fig.add_subplot(111)
	ax.plot(x,y)
	# leg = ax.legend(('Model length'), 'upper center', shadow=True)
	
	ax.grid(False)  
	ax.set_ylabel('100 * (High - Low) / Close')

	title = gen_title(symbol, 'Intra-Day Range as a Percentage of Closing Price', slice_start_date, slice_end_date)
	ax.set_title(title)

	# date intervals & markers
	(formatter, locator) = tick_info(slice_start_date, slice_end_date)
	ax.xaxis.set_major_formatter(formatter) 
	ax.xaxis.set_major_locator(locator)
	fever_fig.autofmt_xdate(rotation=90)
	ax.set_xlim([slice_start_date, slice_end_date])
	ax.set_xlabel('Date')
	
	# ------------
	
	h = Histogram(delta)
	left_edge = []
	height = []
	for bin in h.bins:
		left_edge.append(float(bin.floor))
		height.append(h.bin_contrib_perc(bin))
	
	x = np.array(left_edge)
	y = np.array(height)
	
	dist_fig = plt.figure()
	ax = dist_fig.add_subplot(111)
	ax.bar(x, y, width=h.bins[0].range)
	
	ax.set_xlim(h.min, h.max)
	ax.set_ylabel('% of Population')
	ax.set_xlabel('Intra-Day Range i.t.o Close : 100 * (High - Low) / Close')

	title = gen_title(symbol, 'Distribution of Intra-Day Range', slice_start_date, slice_end_date)
	ax.set_title(title)

	return fever_fig, dist_fig
 
def analyse(symbol, start_date, end_date, dates, openn, high, low, close, volume, output_root, gen_title):
	
	analyses = []
		
	analyser = OHLCVAnalysis(dates, openn, high, low, close, volume, start_date, end_date)
	report = analyser.report()
	analyses.append(Analysis('Summary', None, report))
	
	# ----------------------------------------------------------------
	# LINEAR 
	# ----------------------------------------------------------------
	
	# CLOSE, VOLUME TIME SERIES
	
	# price, volume as a fn of time
	#
	price_vol_fig = gen_dual_series_scatter_plot(symbol, dates, close, volume, start_date, end_date, gen_title)    
	price_vol_fig_img_file_name = 'price_volume.png'
	save_path = output_root + '/' + price_vol_fig_img_file_name
	price_vol_fig.savefig(save_path) 
	analyses.append(Analysis('Price-Vol Time Series', price_vol_fig_img_file_name, []))  
	
	# OPEN TO CLOSE MOVE
	
	(move_fever_fig, move_dist_fig) = analyse_daily_open_to_close_movement(symbol, dates, openn, close, start_date, end_date, gen_title)
	
	move_fever_fname = 'move_fever.png'  
	save_path = output_root + '/' + move_fever_fname
	move_fever_fig.savefig(save_path)
	analyses.append(Analysis('Day Move Fever', move_fever_fname, []))
	
	move_dist_fname = 'move_dist.png'  
	save_path = output_root + '/' + move_dist_fname
	move_dist_fig.savefig(save_path)
	analyses.append(Analysis('Distribution of Daily Moves', move_dist_fname, []))
	
	# INTRADAY VOLATILITY
	
	fever_fig, dist_fig = gen_intraday_volatility_plots(symbol, dates, high, low, close, start_date, end_date, gen_title)    
	
	intraday_volatility_fever_fname = 'intraday_volatility_fever.png'  
	save_path = output_root + '/' + intraday_volatility_fever_fname
	fever_fig.savefig(save_path)
	analyses.append(Analysis('Intra-Day Range Fever', intraday_volatility_fever_fname, []))
	
	intraday_volatility_dist_fname = 'intraday_volatility_dist.png'  
	save_path = output_root + '/' + intraday_volatility_dist_fname
	dist_fig.savefig(save_path)
	analyses.append(Analysis('Distribution of Intra-day Range', intraday_volatility_dist_fname, []))
	
	# ----------------------------------------------------------------
	# LOGARITHMIC
	
	lopen = [math.log(x) for x in openn]
	lhigh = [math.log(x) for x in high]
	llow = [math.log(x) for x in low]
	lclose = [math.log(x) for x in close] 
	lvol = [math.log(x) if x > 0 else 0 for x in volume]    
	
	# LOG CLOSE TIME SERIES
	
	log_price_vol_fig = gen_dual_series_scatter_plot(symbol, dates, lclose, lvol, start_date, end_date, gen_title)    
	log_price_vol_fig_img_file_name = 'log_price_volume.png'
	save_path = output_root + '/' + log_price_vol_fig_img_file_name
	log_price_vol_fig.savefig(save_path) 
	analyses.append(Analysis('Log Price Time Series', log_price_vol_fig_img_file_name, []))  
	
	# LOG INTRA-DAY RANGE
	
	log_fever_fig, log_dist_fig = gen_intraday_volatility_plots(symbol, dates, lhigh, llow, lclose, start_date, end_date, gen_title)      
	log_intraday_volatility_fever_fname = 'log_intraday_volatility_fever.png'  
	save_path = output_root + '/' + log_intraday_volatility_fever_fname
	log_fever_fig.savefig(save_path)
	analyses.append(Analysis('Log Intra-Day Range Fever', log_intraday_volatility_fever_fname, []))  
 
	return analyses

def tick_info(slice_start_date, slice_end_date):
	'''
	return appropriate - visually attractive and informative - (formatter, locator) for data series
	'''  

	duration = slice_end_date - slice_start_date  
	day_count = abs(duration.days)

	desired_interval_count = 10
	interval_day_length = day_count / desired_interval_count
	formatter = None # '%Y-%m-%d'
	locator = None  

	if interval_day_length > 365:    		
		year_tick = int(interval_day_length / 365)
		formatter = mpl.dates.DateFormatter('%Y')
		locator = mpl.dates.YearLocator(year_tick)
		interval_year_length = interval_day_length / 365
	elif interval_day_length > 30:
		formatter = mpl.dates.DateFormatter('%Y-%m')
		interval_month_length = interval_day_length / 30
		locator = mpl.dates.MonthLocator(interval=int(interval_month_length))
	else:
		formatter = mpl.dates.DateFormatter('%Y-%m-%d')
		locator = mpl.dates.DayLocator(interval=int(interval_day_length))  
	return (formatter, locator)

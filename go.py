import argparse

from datetime import datetime
import matplotlib

import csv
from plotter import gen_analyses

def load_csv_rows(source_path, start_date, end_date, timestamp_format = '%Y-%m-%d'):

	rows = []

	col_map = {}

	with open(source_path) as csv_file:
	    
	    dialect = csv.Sniffer().sniff(csv_file.read(1024))
	    csv_file.seek(0)
	    reader = csv.reader(csv_file, dialect)

	    header_skipped = False
	    for row in reader:

	    	if not header_skipped:
	    		header_skipped = True
	    		
	    		col_count = len(row) 

	    		for i in range(col_count):

	    			col_name = row[i].lower().strip()
	    			col_map[col_name] = i

	    		continue

	    	timestamp = datetime.strptime(row[col_map['date']], timestamp_format)

	    	if start_date:
	    		if (timestamp < start_date):
	    			continue
	    	if end_date:
	    		if (timestamp > end_date):
	    			break

	    	row_data = []
	    	for j in range(col_count):
	    		value = row[j]
	    		if j == col_map['date']:
	    			value = datetime.strptime(value, timestamp_format)
    			row_data.append(value)

    		rows.append(row_data)
	    	
	return col_map, rows

def load_columns(source_path, start_date, end_date):

	col_map, rows = load_csv_rows(source_path, start_date, end_date)

	dates = []
	high = []
	low = []
	openn = []
	close = []
	volume = []

	for row in rows:
		dates.append(row[col_map['date']])
		high.append(float(row[col_map['high']]))
		low.append(float(row[col_map['low']]))
		openn.append(float(row[col_map['open']]))
		close.append(float(row[col_map['close']]))
		volume.append(float(row[col_map['volume']]))

	return (dates, high, low, openn, close, volume)

def analyse(source_path, start_date, end_date, label, out_root):

	start_date = datetime.strptime(start_date, '%Y-%m-%d') 
	end_date = datetime.strptime(end_date, '%Y-%m-%d')

	(dates, high, low, openn, close, volume) = load_columns(source_path, start_date, end_date)

	file_name = label.replace(' ', '') + '.png'

	gen_analyses(label, start_date, end_date, dates, openn, high, low, close, volume, out_root)

# plt.savefig(file_name, bbox_inches='tight')
#analyse()

def get_analysis_parameters():

	print('mart - real time market analysis')

	parser = argparse.ArgumentParser(prog='mart')

	parser.add_argument('--data_path', help='source data set file path', required=True)
	parser.add_argument('--out_path', help='report output path', required=True)
	parser.add_argument('--start_date', help='sample start date', required=True)
	parser.add_argument('--end_date', help='sample end date', required=True)
	parser.add_argument('--label', help='data set label')

	values = parser.parse_args()

	data_path = values.data_path
	out_path = values.out_path
	label = values.label
	start_date = values.start_date
	end_date = values.end_date

	return (data_path, start_date, end_date, label, out_path)

def go():
	
	(data_path, start_date, end_date, label, out_path) = get_analysis_parameters()
	analyse(data_path, start_date, end_date, label, out_path)

go()
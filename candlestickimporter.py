import csv
import datetime

def parse_string_to_date(date_str):
    '''parse date string of format 'yyyy-mm-dd' to datetime.date'''
    
    tokens = date_str.split('-')
    y = int(tokens[0].lstrip('0'))
    m = int(tokens[1].lstrip('0'))
    d = int(tokens[2].lstrip('0'))
    
    return datetime.date(y, m, d)
    
def row_to_dict(row):
    '''return dict with keys [date, open, high, low, close, volume, adj_close]'''
    date = parse_string_to_date(row[0])
    
    open = float(row[1])
    high = float(row[2])
    low = float(row[3])
    close = float(row[4])
    
    volume = long(row[5])
    
    adj_close = float(row[6])
    
    return {'date' : date, 'open' : open, 'high' : high, 'low' : low, 'close' : close, 'adj_close' : adj_close, 'volume' : volume }

def load_csv_data_rows(path_to_csv):
    '''load specified csv file, return list of rows (including header row, if any)'''

    data_rows = []
    
    csv_file = open(path_to_csv, 'r')
    reader = csv.reader(csv_file)

    data_rows = []

    line_count = 0
    exit_loop = False;
    while exit_loop == False:
        try:
            row = reader.next()
            data_rows.append(row)
            line_count += 1
        except StopIteration:
            exit_loop = True

    csv_file.close()

    return data_rows
    
def parse_rows_to_distinct_lists(data_rows, clip_first_line=True):
    '''
    return (date, open, high, low, close, adj_close, volume) from list of data_rows
    '''

    date, open, high, low, close, adj_close, volume = [], [], [], [], [], [], []

    start_idx = 0
    if clip_first_line == True:
        start_idx = 1
    
    for i in range(start_idx, len(data_rows)):

        r = row_to_dict(data_rows[i])

        date.append(r['date'])
        open.append(r['open'])
        high.append(r['high'])
        low.append(r['low'])
        close.append(r['close'])
        adj_close.append(r['adj_close'])
        volume.append(r['volume'])    

    return date, open, high, low, close, adj_close, volume
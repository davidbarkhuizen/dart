

# load configs

# load from CSV flat file
# clean - e.g. date format
# merge

# filter - start date, end date, columns

# analyse (produces reports)
# persist reports


def load_data_config():
	return None

def load(data_config):
	pass

def clean(dirty):
	return dirty

def merge(data):
	return data

def filter_(data):
	return data

def analyse(data, config):
	reports = []
	return reports

def persist_reports(reports):
	pass

def program(config_path='config/data.config.json'):

	data_config = load_data_config(config_path)

	raw_data = load(config)
	clean_data = clean(raw_data)
	merged_data = merge(clean_data)
	
	filtered_data = filter_(merged_data)
	
	reports = analyse(filtered_data, config)
	persist_reports(reports, config)

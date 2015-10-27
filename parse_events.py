import pandas as pd
import dateutil.parser
#import statsmodels.formula.api as sm

def convert_tstamp(df, col_index):
	df[col_index] = pd.to_datetime(df.apply(lambda row: row[col_index], axis=1))
	return

data = pd.read_csv('data/events_train.csv')
# basic cleaning
data = data[pd.notnull(data['event_id'])]
data = data[pd.notnull(data['event_description'])]
data = data[pd.notnull(data['start_tstamp'])]
data = data[pd.notnull(data['confirmed_tstamp'])]
data = data[pd.notnull(data['created_tstamp'])]
data = data[pd.notnull(data['closed_tstamp'])]
data = data[pd.notnull(data['event_type'])]
data = data[pd.notnull(data['event_subtype'])]
data = data[pd.notnull(data['location'])]
data = data[pd.notnull(data['latitude'])]	#	y
data = data[pd.notnull(data['longitude'])]	#	x
data = data[pd.notnull(data['number_of_responders'])]
data = data[pd.notnull(data['lanes_affected'])]

bound_cols = ['ymin', 'xmin', 'ymax', 'xmax', 'begin', 'end']
bounds = pd.read_csv('data/prediction_trials.tsv', sep='\t', names=bound_cols)

convert_tstamp(bounds, 'begin')
convert_tstamp(bounds, 'end')

convert_tstamp(data, 'created_tstamp')
convert_tstamp(data, 'confirmed_tstamp')
convert_tstamp(data, 'closed_tstamp')
convert_tstamp(data, 'start_tstamp')

data['month']=data.apply(lambda row: row['created_tstamp'].month, axis=1)
data['year']=data.apply(lambda row: row['created_tstamp'].year, axis=1)
bounds['bound_month']=bounds.apply(lambda row: row['begin'].month, axis=1)
bounds['bound_year']=bounds.apply(lambda row: row['begin'].year, axis=1)

joined = data.join(bounds)

groups = data.groupby(['event_type', 'ymin', 'xmin', 'ymax', 'xmax'])

for key, group in groups:
	# Filter Out All Events Not In Boundry Box
	group = group[group['latitude'] >= key['ymin'] & group['latitude'] <= key['ymax']) & (group['longitude'] >= key['xmin'] & group['longitude'] <= key['xmax']]
	print key



print data[:5]
print bounds['end'][:5]
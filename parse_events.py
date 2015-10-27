import pandas as pd
import dateutil.parser
import statsmodels.formula.api as sm

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

eventTypes = data.groupby(['event_type'])
boundBox = bounds.groupby(['ymin', 'xmin', 'ymax', 'xmax'])

for bounds in boundBox:
	for event, eventType in eventTypes:
			# Filter Out All Events Not In Boundry Box
			eventType = eventType[eventType['latitude'] >= bounds['ymin'] && eventType['latitude'] <= bounds['ymax']) && (eventType['longitude'] >= bounds['xmin'] && eventType['longitude'] <= bounds['xmax']]
			



print data['created_tstamp'][:5]
print bounds['end'][:5]
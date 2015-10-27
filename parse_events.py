import pandas as pd
import dateutil.parser

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

eventTypes = data.groupby(['event_type'])
boundBox = bounds.groupby(['ymin', 'xmin', 'ymax', 'xmax', 'bound_month'])

eventsInBox = pd.DataFrame(columns=('eventType', 'numEvents','month', 'year', 'xmin', 'xmax', 'ymin', 'ymax'))


for boundKey, bounds in boundBox:
	ymin = bounds['ymin'][bounds['ymin'].keys()[0]]
	xmin = bounds['xmin'][bounds['xmin'].keys()[0]]
	ymax = bounds['ymax'][bounds['ymax'].keys()[0]]
	xmax = bounds['xmax'][bounds['xmax'].keys()[0]]
	month = bounds['bound_month'][bounds['bound_month'].keys()[0]]
	print "\nBounds: ", xmin, xmax, ymin, ymax
	for event, eventType in eventTypes:
		# Filter Out All Events Not In Boundry Box
		eventType = eventType[eventType['latitude'] >= ymin]
		eventType = eventType[eventType['latitude'] <= ymax]
		eventType = eventType[eventType['longitude'] >= xmin]
		eventType = eventType[eventType['longitude'] <= xmax]
		eventType = eventType[eventType['month'] == month]

		yearlyGroup = eventType.groupby(['year'])
		for year, eventsInYear in yearlyGroup:
			temp = pd.DataFrame({'eventType': [event] , 'numEvents': [len(eventsInYear)], 'month': [month], 'year':[year], 'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax})
			eventsInBox = eventsInBox.append(temp)

			





print data['created_tstamp'][:5]
print bounds['end'][:5]
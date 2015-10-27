import pandas as pd
import dateutil.parser
import time
import csv

def convert_tstamp(df, col_index):
	df[col_index] = pd.to_datetime(df.apply(lambda row: row[col_index], axis=1))
	return

start_time = time.time()
data = pd.read_csv('data/events_train.csv')
# basic cleaning
data = data[pd.notnull(data['created_tstamp'])]
data = data[pd.notnull(data['event_type'])]
data = data[pd.notnull(data['latitude'])]	#	y
data = data[pd.notnull(data['longitude'])]	#	x
data = data[data['location'] != 'test']

bound_cols = ['ymin', 'xmin', 'ymax', 'xmax', 'begin', 'end']
bounds = pd.read_csv('data/prediction_trials.tsv', sep='\t', names=bound_cols)

convert_tstamp(bounds, 'begin')
convert_tstamp(bounds, 'end')

convert_tstamp(data, 'created_tstamp')

print 'Beginning Time Consuming Lambdas'
print len(data)

data['month']=data.apply(lambda row: row['created_tstamp'].month, axis=1)
data['year']=data.apply(lambda row: row['created_tstamp'].year, axis=1)
bounds['bound_month']=bounds.apply(lambda row: row['begin'].month, axis=1)
bounds['bound_year']=bounds.apply(lambda row: row['begin'].year, axis=1)

eventTypes = data.groupby(['event_type'])
boundBox = bounds.groupby(['ymin', 'xmin', 'ymax', 'xmax', 'bound_month'])

eventsInBox = pd.DataFrame(columns=('eventType', 'numEvents','month', 'year', 'xmin', 'xmax', 'ymin', 'ymax'))

print 'Done Processing. Beginning Main Loop.'
counter = 1
size = 0
for boundKey, bounds in boundBox:
	size+=1
print size

for boundKey, bounds in boundBox:
	ymin = bounds['ymin'][bounds['ymin'].keys()[0]]
	xmin = bounds['xmin'][bounds['xmin'].keys()[0]]
	ymax = bounds['ymax'][bounds['ymax'].keys()[0]]
	xmax = bounds['xmax'][bounds['xmax'].keys()[0]]
	month = bounds['bound_month'][bounds['bound_month'].keys()[0]]
	print counter, '/', size
	counter += 1
	#print "\nBounds: ", xmin, xmax, ymin, ymax
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

		
eventsInBox.to_csv("out.csv", quoting=csv.QUOTE_NONE, encoding='utf-8', index = False)
print "My program took", time.time() - start_time, "to run"
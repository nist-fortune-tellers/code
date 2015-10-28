import pandas as pd
import dateutil.parser
import time
import csv
import os

def convert_tstamp(df, col_index):
	df[col_index] = pd.to_datetime(df.apply(lambda row: row[col_index], axis=1))
	return

#Create Output Path if it does Not Exist
if not os.path.exists('output'):
    os.makedirs('output')

#Open Files for Writing CSV
csvFile = open('output/aggregated_events.csv', 'w')
csvWriter = csv.writer(csvFile)
# Write First Header Column
csvWriter.writerow(['eventType', 'numEvents', 'month', 'year', 'xmin', 'xmax', 'ymin', 'ymax'])

start_time = time.time()
data = pd.read_csv('data/events_train.csv')

print 'Beginning Basic Cleaning'

# basic cleaning
data = data[pd.notnull(data['created_tstamp'])]
data = data[pd.notnull(data['event_type'])]
data = data[pd.notnull(data['latitude'])]	#	y
data = data[pd.notnull(data['longitude'])]	#	x
data = data[data['location'] != 'test']

bound_cols = ['ymin', 'xmin', 'ymax', 'xmax', 'begin', 'end']
bounds = pd.read_csv('data/prediction_trials.tsv', sep='\t', names=bound_cols)

print 'Timestamp Conversion'
convert_tstamp(bounds, 'begin')
convert_tstamp(bounds, 'end')

data['old_tstamp'] = data['created_tstamp']
convert_tstamp(data, 'created_tstamp')

print 'Lambda 1/4'
data['month']=data.apply(lambda row: row['created_tstamp'].month, axis=1)
print 'Lambda 2/4'
data['year']=data.apply(lambda row: row['created_tstamp'].year, axis=1)
print 'Lambda 3/4'
bounds['bound_month']=bounds.apply(lambda row: row['begin'].month, axis=1)
print 'Lambda 4/4'
bounds['bound_year']=bounds.apply(lambda row: row['begin'].year, axis=1)

print 'Group Bys'
eventTypes = data.groupby(['event_type'])
boundBox = bounds.groupby(['ymin', 'xmin', 'ymax', 'xmax', 'bound_month'])

eventsInBox = pd.DataFrame(columns=('eventType', 'numEvents','month', 'year', 'xmin', 'xmax', 'ymin', 'ymax'))

print 'Done Processing. Beginning Main Loop.'

counter = 1
size = 0

for _, _ in boundBox:
	size+=1
fsize=float(size)

print counter, '/', size
for boundKey, bounds in boundBox:
	ymin = bounds['ymin'][bounds['ymin'].keys()[0]]
	xmin = bounds['xmin'][bounds['xmin'].keys()[0]]
	ymax = bounds['ymax'][bounds['ymax'].keys()[0]]
	xmax = bounds['xmax'][bounds['xmax'].keys()[0]]
	month = bounds['bound_month'][bounds['bound_month'].keys()[0]]
	#Print Every 100 (since this runs slowwww)
	if counter % 100 == 0:
		print counter, '/', size, '-', int((counter/fsize)*100), '%'
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
			csvWriter.writerow([event, len(eventsInYear), month, year, xmin, xmax, ymin, ymax])

csvFile.close()
print "My program took", time.time() - start_time, "to run"
import pandas as pd
import time
import csv

def convert_tstamp(df, col_index):
	df[col_index] = pd.to_datetime(df.apply(lambda row: row[col_index], axis=1))
	return
def compare(desired, actual, decimal):
	return abs(desired-actual) < 0.5 * 10**(-decimal)

start_time = time.time()

print 'Look Into My Crystal Ball......'

#Open Files for Writing CSV
csvFile = open('output/prediction_submissions_3.txt', 'w')
csvWriter = csv.writer(csvFile, delimiter='\t')

bound_cols = ['ymin', 'xmin', 'ymax', 'xmax', 'begin', 'end']
bounds = pd.read_csv('data/prediction_trials.tsv', sep='\t', names=bound_cols)

predicted  = pd.read_csv('output/linear_funcs.csv')	
# Keys: 'eventType','month', 'xmin', 'xmax', 'ymin', 'ymax', 'intercept', 'slope'

print 'Converting Timestamps (Applying Lambdas)'
convert_tstamp(bounds, 'begin')
bounds['month']=bounds.apply(lambda row: row['begin'].month, axis=1)
bounds['year']=bounds.apply(lambda row: row['begin'].year, axis=1)

size = len(bounds)
fsize = float(size)
counter = 1

# Events in Order for Printing
events = ['accidentsAndIncidents', 'roadwork', 'precipitation', 'deviceStatus', 'obstruction', 'trafficConditions']
numEvents = len(events)

print 'Begin Main Loop'
for x in range(0, len(bounds)):

	#Print Every 100
	if counter % 100 == 0:
		print 'Predicting Future:', counter, '/', size, '-', int((counter/fsize)*100), '%'
	counter += 1

	ymin = bounds['ymin'][x]
	xmin = bounds['xmin'][x]
	ymax = bounds['ymax'][x]
	xmax = bounds['xmax'][x]
	month = bounds['month'][x]
	year = bounds['year'][x]

	ptemp = predicted

	ptemp = ptemp[compare(ymin, ptemp['ymin'], 6)]
	ptemp = ptemp[compare(ymax, ptemp['ymax'], 6)]
	ptemp = ptemp[compare(xmin, ptemp['xmin'], 6)]
	ptemp = ptemp[compare(xmax, ptemp['xmax'], 6)]
	ptemp = ptemp[ptemp['month'] == month]

	#Exclusion Test
	excluTest = excluTest.append(ptemp)

	#Eventual Output For Eevents
	eventOutput = []

	#Build Output
	for event in events:
		etemp = ptemp[ptemp['eventType'] == event]
		# Handle Zero Case
		if len(etemp) == 0:
			eventOutput.append(0)
			continue

		# Print Warning on Multiple
		if len(etemp) > 1:
			print 'Warning: More than one event found in a (box,month) pair. Possible Rounding Issues. Using First Value.'
			print 'Erronous Value: ', ptemp

		# Now retrieve the relevant values!
		intercept = etemp['intercept'][etemp['intercept'].keys()[0]]
		slope = etemp['slope'][etemp['slope'].keys()[0]]

		#Perform Calculation! (y = mx+b)
		result = float(intercept) + float(slope)*float(year)
		#Do some simple sanity tests
		if result < 0:
			#Oh No! result < 0. Defaulting value to 0.			
			result = 0
		else:
			#Round Result to nearest whole number
			result = int(round(result, 0))

		#Append Result to Output Array!
		eventOutput.append(result)

	# Now that we've added all events, we can write them to the csv!
	csvWriter.writerow(eventOutput)


csvFile.close()
print "My program took", time.time() - start_time, "to run"
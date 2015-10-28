import pandas as pd
import time
import csv

def convert_tstamp(df, col_index):
	df[col_index] = pd.to_datetime(df.apply(lambda row: row[col_index], axis=1))
	return
def compare(desired, actual, decimal):
	return abs(desired-actual) < 0.5 * 10**(-decimal)

start_time = time.time()

bound_cols = ['ymin', 'xmin', 'ymax', 'xmax', 'begin', 'end']
bounds = pd.read_csv('data/prediction_trials.tsv', sep='\t', names=bound_cols)
predicted  = pd.read_csv('output/predicted.csv')	#'eventType','month', 'xmin', 'xmax', 'ymin', 'ymax', 'intercept', 'slope'

convert_tstamp(bounds, 'begin')
bounds['month']=bounds.apply(lambda row: row['begin'].month, axis=1)
bounds['year']=bounds.apply(lambda row: row['begin'].year, axis=1)

# predicted['ymin_r']=predicted.apply(lambda row: round(row['ymin'], 4), axis=1)
# predicted['xmin_r']=predicted.apply(lambda row: round(row['xmin'], 4), axis=1)
# predicted['ymax_r']=predicted.apply(lambda row: round(row['ymax'], 4), axis=1)
# predicted['xmax_r']=predicted.apply(lambda row: round(row['xmax'], 4), axis=1)
# print predicted[:5]

for x in range(0, len(bounds)):
	bound = bounds.iloc[[x]]
	ymin = bound['ymin'][x]
	xmin = bound['xmin'][x]
	ymax = bound['ymax'][x]
	xmax = bound['xmax'][x]
	month = bound['month'][x]
	year = bound['year'][x]

	#print ymin, xmin, ymax, xmax, month, year
	ptemp = predicted

	pymin = round(ptemp['ymin'][0], 4)
	#print pymin


	ptemp = ptemp[compare(ymin, ptemp['ymin'], 6)]
	ptemp = ptemp[compare(ymax, ptemp['ymax'], 6)]
	ptemp = ptemp[compare(xmin, ptemp['xmin'], 6)]
	ptemp = ptemp[compare(xmax, ptemp['xmax'], 6)]
	ptemp = ptemp[ptemp['month'] == month]

	if len(ptemp) > 0:
		print ptemp

	
	





print "My program took", time.time() - start_time, "to run"
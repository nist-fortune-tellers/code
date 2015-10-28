import pandas as pd
import time
import csv
import statsmodels.formula.api as sm

start_time = time.time()
eventsInBox = pd.read_csv('output/aggregated.tsv', sep='\t')

groupedEvents = eventsInBox.groupby(['eventType', 'month', 'xmin', 'ymin', 'xmax', 'ymax'])		#gives eventtype of a month in a bounding box

for key, group in groupedEvents:
	yearMin = group['year'].min()
	yearMax = group['year'].max()
	for x in range(yearMin, yearMax):
		if len(group[group['year'] == x]) == 0:
			temp = pd.DataFrame({'numEvents': [0], 'year': [x]})
			group = group.append(temp)

	result = sm.ols(formula="numEvents ~ year", data=group).fit()
	print '\n=========================='
	print 'KEY: '
	print key
	print 'RESULT: '
	print result.params['Intercept']
	print result.params['year']
	print '=========================='











print "My program took", time.time() - start_time, "to run"
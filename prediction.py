import pandas as pd
import time
import csv
import statsmodels.formula.api as sm

start_time = time.time()
eventsInBox = pd.read_csv('output/aggregated.csv')

groupedEvents = eventsInBox.groupby(['eventType', 'month', 'xmin', 'ymin', 'xmax', 'ymax'])		#gives eventtype of a month in a bounding box

predictedEvents = pd.DataFrame(columns=('eventType','month', 'xmin', 'xmax', 'ymin', 'ymax', 'intercept', 'slope'))
size = 0
for _, _ in groupedEvents:
	size += 1

counter = 1
for key, group in groupedEvents:
	print counter, '/', size
	counter += 1
	yearMin = group['year'].min()
	yearMax = group['year'].max()
	ymin = group['ymin'][group['ymin'].keys()[0]]
	xmin = group['xmin'][group['xmin'].keys()[0]]
	ymax = group['ymax'][group['ymax'].keys()[0]]
	xmax = group['xmax'][group['xmax'].keys()[0]]
	eventType = group['eventType'][group['eventType'].keys()[0]]
	month = group['month'][group['month'].keys()[0]]
	for x in range(yearMin, yearMax):
		if len(group[group['year'] == x]) == 0:
			temp = pd.DataFrame({'numEvents': [0], 'year': [x]})
			group = group.append(temp)

	result = sm.ols(formula="numEvents ~ year", data=group).fit()
	temp = pd.DataFrame({'eventType': [eventType], 'month': [month], 'xmin': [xmin], 'xmax': [xmax], 'ymin': [ymin], 'ymax': [ymax], 'intercept': [result.params['Intercept']], 'slope': [result.params['year']]})
	predictedEvents = predictedEvents.append(temp)


predictedEvents.to_csv("output/predicted.csv", quoting=csv.QUOTE_NONE, encoding='utf-8', index = False)










print "My program took", time.time() - start_time, "to run"
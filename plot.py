import pandas as pd
import matplotlib.pyplot as plt

print 'Grouping'

eventsInBox = pd.read_csv('output/reference_aggregated_events.csv')
groupedEvents = eventsInBox.groupby(['xmin', 'ymin', 'xmax', 'ymax', 'month', 'eventType'])

print 'Done Grouping'
onlyPlot = 20
max1 = -1
max2 = -1
max3 = -1
numEvents = len(groupedEvents)
currEvent = 1
for key, group in groupedEvents:
	print currEvent, "/", numEvents
	currEvent += 1
	if len(group) >= max1:
		max3 = max2
		max2 = max1
		max1 = len(group)
		
	# if onlyPlot == 0:
	# 	break

	# eventType = group['eventType'][group['eventType'].keys()[0]]
	# xmax = group['xmax'][group['xmax'].keys()[0]]
	# ymax = group['ymax'][group['ymax'].keys()[0]]
	# month = group['month'][group['month'].keys()[0]]
	# title = eventType + str(xmax) + str(ymax) + str(month)
	# if len(group) > 5 and month == 3:
	# 	onlyPlot -= 1
	# 	group.plot(kind='scatter',x='year',y='numEvents', title = title)

print "maxs: ", max1, max2, max3
	

#plt.show()


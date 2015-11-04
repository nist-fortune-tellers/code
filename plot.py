import pandas as pd
import matplotlib.pyplot as plt

eventsInBox = pd.read_csv('output/reference_aggregated_events.csv')
groupedEvents = eventsInBox.groupby(['xmin', 'ymin', 'xmax', 'ymax', 'month', 'eventType'])

onlyPlot = 20
for key, group in groupedEvents:
	if onlyPlot == 0:
		break

	eventType = group['eventType'][group['eventType'].keys()[0]]
	xmax = group['xmax'][group['xmax'].keys()[0]]
	ymax = group['ymax'][group['ymax'].keys()[0]]
	month = group['month'][group['month'].keys()[0]]
	title = eventType + str(xmax) + str(ymax) + str(month)
	if len(group) > 5 and month == 3:
		onlyPlot -= 1
		group.plot(kind='scatter',x='year',y='numEvents', title = title)
	

plt.show()


import pandas as pd
import matplotlib.pyplot as plt

eventsInBox = pd.read_csv('output/aggregated_events.csv')
groupedEvents = eventsInBox.groupby(['eventType', 'month', 'xmin', 'ymin', 'xmax', 'ymax'])


for key, group in groupedEvents:
	group.plot(kind='scatter',x='year',y='numEvents')
	break

plt.show()
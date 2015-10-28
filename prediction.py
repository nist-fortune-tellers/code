import pandas as pd
import time
import csv




start_time = time.time()
eventsInBox = pd.read_csv('data/out.tsv', sep='\t')

print eventsInBox[:3]

eventsInBox.groupby('eventType', 'month', 'xmin', 'ymin', 'xmax', 'ymax')		#gives eventtype of a month in a bounding box
















print "My program took", time.time() - start_time, "to run"
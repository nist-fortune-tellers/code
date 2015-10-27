# Baseline approach for prediction.

import csv
import os
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

if __name__=="__main__":

	# verify files
	assert os.path.isfile('events_train.csv'), "Error: you have to place the events_train.csv file to the script folder."
	assert os.path.isfile('prediction_trials.tsv'), "Error: you have to place the prediction_trials.tsv file to the script folder."

	# read testing cases.
	with open('prediction_trials.tsv','rb') as csvfile:
		tc = [(float(r[1]),float(r[0]),float(r[3]),float(r[2])) for r in csv.reader(csvfile, delimiter='\t')]	# [(xmin,xmax,ymin,ymax)]
	
	# load training data.
	with open('events_train.csv', 'rb') as csvfile:
		rows = [r for r in csv.reader(csvfile, delimiter=',') if r[10].find('.') > -1]
	
	# predict the first 10 testing cases, based on the counts of events in 2014.
	for xmin,xmax,ymin,ymax in tc[:10]:
		cnt = Counter([r[6] for r in rows if r[4].split('-')[0] == '2014' and float(r[10])>xmin and float(r[10])<xmax and float(r[9])>ymin and float(r[9])<ymax])	# {event_type:counts}
		print "%.1f\t%.1f\t%.1f\t%.1f\t%.1f\t%.1f" % (cnt['accidentsAndIncidents']/12.0,cnt['roadwork']/12.0,cnt['precipitation']/12.0,cnt['deviceStatus']/12.0,cnt['obstruction']/12.0,cnt['trafficConditions']/12.0)

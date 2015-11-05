import sys
import numpy as np
import pandas as pd
import math
import re
import string
import os
import time

k = 5280.0/360000.0 # car_length equation constant = 0.14666

def car_length(row):
    speed    = row['speed']
    occ      = row['occupancy']
    interval = row['interval']
    flow     = row['flow']
    
    if flow == 0:
        return 0
    
    return ( k * speed * occ * interval / flow )

def new_flow(row):
    speed      = row['speed']
    occ        = row['occupancy']
    interval   = row['interval']
    flow       = row['flow']
    car_length = row['car_length']
    changed    = row['changed']
    
    if changed is False:
        return flow
    
    new_flow = k * speed * occ * interval / car_length
    return int( round(new_flow, 0) )

def actually_changed(row):
    flow     = row['flow']
    new_flow = row['new_flow']
    
    if flow == new_flow:
        return False
    
    return True

def changed_reason(row):
    changed        = row['actually_changed']
    
    if changed is True:
        return "1"
    
    return ""

if len(sys.argv) < 4:
    print("Must provide three arguments: ./baseline-noinfo.py input_file_path inventory_file_path output_file_path")
    sys.exit(1)

input_file_path     = sys.argv[1]
inventory_file_path = sys.argv[2]
output_file_path    = sys.argv[3]

print("\n\nCurrent date & time " + time.strftime("%c") + ": Computing consistency correction for " + input_file_path)

detector_data  = pd.read_csv(input_file_path)
inventory_data = pd.read_csv(inventory_file_path)[['lane_id', 'zone_id', 'interval']]

data = pd.merge(detector_data, inventory_data, on='lane_id')
del detector_data
del inventory_data

# calculate car_length for each data point
data['car_length'] = data.apply(lambda row: car_length(row), axis=1)

# calculate median and stdev for entire file (using only valid car lengths)
valid_car_lengths = data[ (data['car_length'] > 10) & (data['car_length'] < 35) ]
file_median       = valid_car_lengths['car_length'].median(axis=0)
file_stdev        = valid_car_lengths['car_length'].std(axis=0)

# new DF for storing cleaned data
cleaned_data = pd.DataFrame()

lane_id_group = data.groupby(['lane_id'])
del data
for key, group in lane_id_group:
    valid_car_lengths = group[ (group['car_length'] > 10) & (group['car_length'] < 35) ]
    
    # calculate median and stdev for specific detector (lane)
    if len(valid_car_lengths) == 0:
        median = file_median
        stdev  = file_stdev
    else:
        median = valid_car_lengths['car_length'].median(axis=0)
        if( (median <= file_median - file_stdev) | (median >= file_median + file_stdev) ):
            median = file_median
            stdev  = file_stdev
        
        stdev  = valid_car_lengths['car_length'].std(axis=0)
        if math.isnan(stdev): # only one valid car length found -> no stdev
            stdev = 0.0
    
    # replace any car lengths that are too far from the median (1 stdev)
    car_lengths_vector = group['car_length'].tolist()
    changed_vector     = [False] * len(car_lengths_vector)
    
    vec_len = len(car_lengths_vector)
    for pos in xrange(0, vec_len):
        if( (car_lengths_vector[pos] <= median - stdev) | (car_lengths_vector[pos] >= median + stdev) ):
            car_lengths_vector[pos] = median
            changed_vector[pos] = True
    
    current_lane_id = group['lane_id'].iloc[0]
    
    group['car_length'] = car_lengths_vector  
    group['changed'] = changed_vector
    
    cleaned_data = cleaned_data.append(group)
# end for

# calculate new flow values where necessary
cleaned_data['new_flow']         = cleaned_data.apply(lambda row: new_flow(row), axis=1)
cleaned_data['actually_changed'] = cleaned_data.apply(lambda row: actually_changed(row), axis=1)
cleaned_data['changed_reason']   = cleaned_data.apply(lambda row: changed_reason(row), axis=1)

# sort to match input file order (moved to end)
#cleaned_data.sort(columns=['lane_id'], axis=0, inplace=True)
#cleaned_data.sort(columns=['measurement_start'], axis=0, inplace=True)

output_data = cleaned_data[['lane_id', 'measurement_start', 'speed', 'flow', 'new_flow', 'occupancy', 'quality', 'zone_id', 'interval', 'car_length', 'actually_changed', 'changed_reason']]
del cleaned_data
output_data.rename(columns={'new_flow': 'flow2'}, inplace=True)
output_data.rename(columns={'actually_changed': 'changed'}, inplace=True)

################################################################################

data_points = output_data[['lane_id', 'measurement_start', 'speed', 'flow', 'flow2', 'occupancy', 'quality', 'zone_id', 'interval', 'changed', 'changed_reason']]
del output_data
flow = 'flow2'

#####

# This line takes like 57 seconds to run....
data_points['DateTime'] = data_points.apply(lambda row: pd.Timestamp(row['measurement_start']), axis=1)
 
#List of unique values in the zone_id column
#zonesList = pd.unique(data_points.zone_id.ravel())
zonesList = data_points.groupby('zone_id')
 
# in a 10 minute window, (3 minutes before current point's reading and 3 minutes after)
# flows in the same zone of diff lanes should have similar values
time_delta = pd.Timedelta(minutes=5)
 
#init empty data frame to hold cleaned data
cleaned_data = pd.DataFrame()
#go thru every unique zone
#for zone in zonesList:        
for zone, pointsInThisZone in zonesList:
    #get all datapoints for a unique zone
    pointsInThisZone = data_points[data_points['zone_id'] == zone]
 
    msmnt_start_vec = pointsInThisZone['DateTime'].tolist()
    flow_vec = pointsInThisZone[flow].tolist()
    vec_len = len(msmnt_start_vec)
    changed_vector = pointsInThisZone['changed'].tolist() #[False] * vec_len
    changed_reason_vec = pointsInThisZone['changed_reason'].tolist() #[''] * vec_len
 
    for pos in xrange(0, vec_len):
        #get all readings within a 10minute window
        timeWindowRows = pointsInThisZone[(pointsInThisZone['DateTime'] >= msmnt_start_vec[pos] - time_delta) & (pointsInThisZone['DateTime'] <= msmnt_start_vec[pos] + time_delta)]
        if len(timeWindowRows) == 0:
            continue
         
        currMedian = timeWindowRows[flow].median()
        #get std deviation
        timeWindowSD = timeWindowRows[flow].std(axis=0)
        if (flow_vec[pos] < currMedian - timeWindowSD) | (flow_vec[pos] > currMedian + timeWindowSD):
            #If here, replace with the median
            flow_vec[pos] = int(round(currMedian,0))
            changed_vector[pos] = True
            changed_reason_vec[pos] += '2'
 
    pointsInThisZone['flow3'] = flow_vec
    pointsInThisZone['changed'] = changed_vector
    pointsInThisZone['changed_reason'] = changed_reason_vec
 
    cleaned_data = cleaned_data.append(pointsInThisZone)


output_data = cleaned_data
del cleaned_data

################################################################################

output_data.sort_values(by=['lane_id'], kind='mergesort', inplace=True, axis=0)
output_data.sort_values(by=['measurement_start'], kind='mergesort', inplace=True, axis=0)

output_data = output_data[['changed', 'flow3', 'changed_reason']]
 
 
def printToOutput(row, f): 
    curr = row
    #output if correct or not
    if curr['changed'] is True:
        f.write('0\t')
    else:
        f.write('1\t')
    #output flow
    f.write(str(curr['flow3']) + '\t')
    #reason
    f.write(curr['changed_reason'] + '\n')
 
with open(output_file_path, "wb") as f:
    output_data.apply(lambda row: printToOutput(row, f), axis=1)


#test_output_data = output_data[['lane_id', 'measurement_start', 'speed', 'flow', 'flow2', 'flow3', 'occupancy', 'changed', 'changed_reason']]

## write to file
#outout_file_dir = os.path.dirname(output_file_path)
#if not os.path.exists(outout_file_dir):
    #os.mkdir(outout_file_dir)

#test_output_data.to_csv(output_file_path,index=False)

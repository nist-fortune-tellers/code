# Map-Reduce Algorithm Conversion!
## Pre-MR
Read `detector_lane_inventory.csv` and for each line in the CSV, we get the `lane_id` and `zone_id` and place it in the Hadoop Job as follows: `job.setLong(<lane_ID>, <zone_id>)`
## Map Reduceeeee
### Group by Zone ID
#### Mapper
Retrieve all values from each line, emit(zone_id, all_data)
#### Reducer
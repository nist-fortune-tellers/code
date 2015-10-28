# Basics
## Setup
### Dependencies
You need a working Python/Pip installation.
Use Pip to install the following dependencies:
- `pandas`
- `statsmodels`

### Data
In the `data/` directory, place the `events_train.csv` provided by the NIST group. The prediction groups, `prediction_trials.tsv`, are already provided in the repository.

## Running
Simply navigate to the project directory, and type `./run.sh`. There will be appropriate output and progress indicators.

## Output
Output goes in a dynamically created directory `output/`. There you will find the required `prediction_submissions_3.txt`, along with various other intermediary outputs.

# About The Project

## Techniques
Our general techniques involved using familiar software, along with a multi-stage process. We also used some basic assumptions about the data to improve our ability to process the data quickly. For our prediction, we utilized a linear regression algorithm based on the number of times a particular event occured in previous years for the same month in a given coordinate box. This allowed us to generate a linear function `numEvents = slope*year + intercept` for each (month, event, area) pair, where `slope` and `intercept` are values generated from the training data, and `year` is the year we'd like to predict for the particular month and event.

## Technologies
We utilized Python for the entire project. The two main libraries we used were Pandas and StatsModels. Pandas allowed efficient and easy manipulation of the training data. It simplified our code greatly. StatsModels allowed us to use Panda dataFrames directly to train our linear regression models.

## Pipelines
Our Project is divided into three main pipelines, each with appropriately named python files. 
### Aggregate Events
The first pipeline, `aggregate_events.py`, takes in the raw training data and and counts (or aggregates) the number of each different types of events within each (area, month, year) pair. It then outputs this data to a intermediary csv.
### Generate Linear Functions
The second pipeline, `generate_linear_funcs.py`, takes in each (eventType, area, month, year, numEvents) pair and puts it into a dataframe. We then group by (eventType, area, month), and use the resulting (year, numEvent) pairs to train numEvents as a function of the year. We then output the intercept and slope data to a second intermediary csv.
### Predict Future Events
The final pipeline, `predict_future.py`, utilizes the (eventType, month, area, slope, intercept) pairs generated previously, to generate values for each of the the prediction groups in `prediction_trials.tsv`. To do this, for each (area, month, year) pair in the prediction groups, we find the relevant slope pairs defined above. Then, we cycle through all required eventTypes (accidentsAndIncidents, roadwork, precipitation, deviceStatus, obstruction, trafficConditions) in our relevant slope pairs, plugging in the year to the prediction function to generate each of the predicted number of events for each different type of event. This data is output in the order asked, in tab separated format, in a file called `prediction_submissions_3.txt`. A reference version of this file is available in the `output/` directory called `reference_prediction_submissions_3.txt`. 

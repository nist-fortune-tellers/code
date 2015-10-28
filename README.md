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
We utilized Python for the entire project. The two main libraries we used were Pandas and StatsModels. Pandas allowed efficient and easy manipulation of the training data. It simplified our code greatly. StatsModels allowed us to use Panda dataFrames directly to train our linear regression model.

## Pipelines
Our Project is divided into three main pipelines, each with appropriately named python files. 
### Aggregate Events
The first pipline, `aggregate_events.py`, takes in the raw training data and and counts (or aggregates) the number of each different types of event within each (area, month) pair.

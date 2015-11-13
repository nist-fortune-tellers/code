#!/bin/sh
python aggregate_events.py 2014 && \
python generate_linear_funcs.py 2014  && \
python predict_future.py 2014

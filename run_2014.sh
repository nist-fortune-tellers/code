#!/bin/sh
python aggregate_events_2014.py && \
python generate_linear_funcs.py  && \
python predict_future_2014.py

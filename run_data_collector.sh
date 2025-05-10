#!/bin/bash

# Navigate to the project directory
cd "$HOME/Projects/XRP-LP-Rebalancer"

# Activate the xrp virtual environment
source xrp/bin/activate

# Run the data collector script
python data_collector.py

# Deactivate virtual environment
deactivate

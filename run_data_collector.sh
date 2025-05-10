#!/bin/bash

# Navigate to the project directory
cd "$HOME/Projects/XRP-LP-Rebalancer"

# Activate the xrp virtual environment
source "$HOME/Projects/XRP-LP-Rebalancer/xrp/bin/activate"

# Run the data collector script with full path to Python
"$HOME/Projects/XRP-LP-Rebalancer/xrp/bin/python" data_collector.py

# Deactivate virtual environment
deactivate

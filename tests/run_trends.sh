#!/bin/bash
# Script to run the Google Trends updater with virtual environment

# Activate virtual environment
source venv/bin/activate

# Run the Python script
python3 trends_updater.py

# Deactivate virtual environment (optional)
deactivate

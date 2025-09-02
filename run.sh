#!/bin/bash
# Main runner script for Google Trends Data Collector

echo "🚀 Starting Google Trends Data Collector..."

# Activate virtual environment
source venv/bin/activate

# Run the main script
python3 main.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Data collection completed successfully!"
else
    echo "❌ Data collection failed!"
    exit 1
fi

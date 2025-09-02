#!/bin/bash
# Script to run the extended trends updater with virtual environment

echo "🚀 Spúšťam rozšírenú verziu Google Trends updater..."
echo "📊 Budú sa sťahovať: Interest Over Time, Related Topics, Related Queries"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run the extended Python script
python3 trends_updater_extended.py

# Deactivate virtual environment (optional)
deactivate

echo ""
echo "✅ Rozšírená aktualizácia dokončená!"

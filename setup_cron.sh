#!/bin/bash
# Helper script to show the correct cron job command for your setup

echo "🔍 Your current project path:"
echo "   $(pwd)"
echo ""

echo "📋 Copy this line to your crontab (crontab -e):"
echo "   0 3 * * 1 $(pwd)/run_trends.sh >> $(pwd)/trends_updater.log 2>&1"
echo ""

echo "⚡ Quick setup command:"
echo "   echo \"0 3 * * 1 $(pwd)/run_trends.sh >> $(pwd)/trends_updater.log 2>&1\" | crontab -"
echo ""

echo "📝 This will run the script every Monday at 3:00 AM"

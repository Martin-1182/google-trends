#!/bin/bash
# Script to show different cron job frequency options

PROJECT_PATH=$(pwd)

echo "📅 RÔZNE FREKVENCIE CRON JOB:"
echo "=============================="
echo ""

echo "🔸 Súčasná frekvencia (každý pondelok o 3:00):"
echo "   0 3 * * 1 $PROJECT_PATH/run_trends.sh >> $PROJECT_PATH/trends_updater.log 2>&1"
echo ""

echo "🔸 Alternatívne frekvencie:"
echo ""

echo "   📅 Každý deň o 3:00 ráno:"
echo "   0 3 * * * $PROJECT_PATH/run_trends.sh >> $PROJECT_PATH/trends_updater.log 2>&1"
echo ""

echo "   📅 Každú stredu o 2:00 ráno:"
echo "   0 2 * * 3 $PROJECT_PATH/run_trends.sh >> $PROJECT_PATH/trends_updater.log 2>&1"
echo ""

echo "   📅 Každý prvý deň v mesiaci o 6:00 ráno:"
echo "   0 6 1 * * $PROJECT_PATH/run_trends.sh >> $PROJECT_PATH/trends_updater.log 2>&1"
echo ""

echo "   📅 Každé 3 dni o 4:00 ráno:"
echo "   0 4 */3 * * $PROJECT_PATH/run_trends.sh >> $PROJECT_PATH/trends_updater.log 2>&1"
echo ""

echo "⚠️  Pre testovanie (každú hodinu) - NEPOUŽÍVAJTE NA PRODUKCII:"
echo "   0 * * * * $PROJECT_PATH/run_trends.sh >> $PROJECT_PATH/trends_updater.log 2>&1"
echo ""

echo "🔧 Pre zmenu frekvencie:"
echo "   crontab -e"
echo "   # Upravte príslušný riadok"

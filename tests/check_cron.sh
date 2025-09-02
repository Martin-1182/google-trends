#!/bin/bash
# Script to check cron job status and test the setup

echo "🔍 Kontrola cron job nastavenia"
echo "================================"
echo ""

echo "1. 📋 Aktuálne cron joby:"
crontab -l
echo ""

echo "2. 📄 Cron daemon status:"
if systemctl is-active --quiet cron; then
    echo "   ✅ Cron daemon beží"
elif systemctl is-active --quiet crond; then
    echo "   ✅ Cron daemon beží (crond)"
else
    echo "   ❌ Cron daemon nebeží"
    echo "   Spustite: sudo systemctl start cron"
fi
echo ""

echo "3. 🧪 Manuálny test skriptu:"
echo "   ./run_trends.sh"
echo ""

echo "4. 📊 Kontrola log súboru:"
echo "   tail -f trends_updater.log"
echo ""

echo "5. ⏰ Čakanie na najbližší cron spustenie:"
echo "   - Nastavené na: každý pondelok o 3:00 ráno"
echo "   - Môžete počkať alebo spustiť manuálne pre test"
echo ""

echo "⚡ Pre okamžitý test:"
echo "   ./run_trends.sh >> trends_updater.log 2>&1 && echo '✅ Skript prešiel'"

# 🚀 Deployment Guide

## Files to Commit to Git
These files should be committed and pushed to your repository:

### ✅ **Core Files (REQUIRED)**
- `trends_updater.py` - Main script
- `requirements.txt` - Python dependencies
- `run_trends.sh` - Convenience script for running
- `README.md` - Documentation
- `.gitignore` - Git ignore rules

### 🔧 **Helper Files (OPTIONAL)**
- `diagnose_connection.py` - Diagnostic script
- `get_service_account_email.py` - Helper script

## Server Setup Steps

### 1. **Clone Repository on Server**
```bash
cd /var/www
git clone <your-repository-url> Google-trends-data
cd Google-trends-data
```

### 2. **Set Up Python Environment**
```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-venv python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 3. **Set Up Google Service Account**
```bash
# Copy your service account JSON file to the server
# This file should NOT be in git repository
cp /path/to/your/service_account.json /var/www/Google-trends-data/service_account.json

# Set proper permissions
chmod 600 service_account.json
```

### 4. **Create Google Sheet**
1. Create a new Google Sheet named "Google Trends Monitoring"
2. Share it with your service account email (get it with: `python3 get_service_account_email.py`)
3. Give "Editor" permissions

### 5. **Test the Setup**
```bash
# Make scripts executable
chmod +x run_trends.sh

# Test the script
./run_trends.sh
```

### 6. **Set Up Cron Job for Automation**
```bash
# Edit crontab
crontab -e

# Add this line for weekly updates (every Monday at 3:00 AM)
0 3 * * 1 /var/www/Google-trends-data/run_trends.sh >> /var/www/Google-trends-data/trends_updater.log 2>&1
```

## File Structure After Setup
```
/var/www/Google-trends-data/
├── trends_updater.py          # Main script
├── requirements.txt           # Dependencies
├── run_trends.sh             # Runner script
├── README.md                 # Documentation
├── .gitignore               # Git ignore rules
├── service_account.json      # ⚠️  NOT IN GIT - add manually
├── venv/                     # ⚠️  NOT IN GIT - created on server
├── trends_updater.log        # ⚠️  NOT IN GIT - generated logs
├── diagnose_connection.py    # Optional diagnostic
└── get_service_account_email.py # Optional helper
```

## Security Notes
- ✅ `service_account.json` is in `.gitignore` - never commit it!
- ✅ Virtual environment is not in git - create on each server
- ✅ Logs are not in git - they contain runtime information
- ✅ Use `chmod 600 service_account.json` for security

## Deployment Checklist
- [ ] Repository cloned on server
- [ ] Python virtual environment created
- [ ] Dependencies installed
- [ ] Service account JSON file copied (not committed!)
- [ ] Google Sheet created and shared
- [ ] Script tested manually
- [ ] Cron job configured
- [ ] Log file monitored

## Troubleshooting
If something doesn't work:
1. Run `./run_trends.sh` manually to see errors
2. Check `/var/www/Google-trends-data/trends_updater.log`
3. Use `python3 diagnose_connection.py` for connection issues
4. Verify service account permissions on Google Sheet

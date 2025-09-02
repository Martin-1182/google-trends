# Deployment Guide - Google Trends Data Monitoring

## 🚀 Server Deployment

### System Requirements
- Linux server (Ubuntu/CentOS)
- Python 3.7+
- Internet connection
- Cron access

## 📦 Files Structure

### Core Files (Required)
```
Google-trends-data/
├── main.py                 # Main data collector
├── related_extractor.py    # Related data extractor
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── run.sh                 # Bash execution script
└── service_account.json   # Google credentials (not in Git)
```

### Utility Files
```
tests/
├── check_cron.sh          # Check cron status
├── cron_examples.sh       # Cron examples  
├── diagnose_connection.py # Connection diagnostics
├── get_service_account_email.py # Service account info
├── run_trends.sh          # Cron execution script
└── setup_cron.sh          # Automated cron setup
```

## 🔧 Installation Steps

### 1. Server Setup
```bash
# Clone repository
git clone https://github.com/Martin-1182/google-trends.git
cd google-trends

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Google API Configuration

#### Service Account Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google Sheets API
4. Create Service Account:
   - IAM & Admin → Service Accounts
   - Create Service Account
   - Download JSON key
   - Save as `service_account.json`

#### Google Sheets Setup
1. Create new Google Sheets document
2. Share with service account email (Editor access)
3. Note the spreadsheet name

### 3. Configuration
Edit `config.py`:
```python
# Essential settings
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_NAME = 'Google Trends Monitoring'

# Keywords to track
KEYWORDS = [
    "online marketing",
    "seo",
    "social media"
]

# Geographic regions
GEO_MAPPING = {
    'Slovensko': 'SK',
    'Česko': 'CZ',
    'Global': ''
}

# Timing
TIMEFRAME = 'today 3-m'
REQUEST_DELAY = 60  # seconds between requests
```

## 🤖 Automation Setup

### Automated Cron Setup
```bash
chmod +x tests/setup_cron.sh
./tests/setup_cron.sh
```

### Manual Cron Setup
```bash
# Edit crontab
crontab -e

# Add daily execution at 9:00 AM
0 9 * * * /var/www/Google-trends-data/tests/run_trends.sh >> /var/log/google_trends.log 2>&1

# Add weekly Related data collection (Monday 10:00 AM)
0 10 * * 1 cd /var/www/Google-trends-data && /usr/bin/python3 related_extractor.py >> /var/log/google_trends_related.log 2>&1
```

### Cron Management
```bash
# Check active cron jobs
./tests/check_cron.sh

# View logs
tail -f /var/log/google_trends.log

# Check cron examples
./tests/cron_examples.sh
```

## 🔍 Testing & Validation

### Connection Testing
```bash
# Test Google API connection
python3 tests/diagnose_connection.py

# Get service account info  
python3 tests/get_service_account_email.py

# Manual execution test
python3 main.py
```

### Troubleshooting
```bash
# Check logs for errors
grep -i error /var/log/google_trends.log

# Test specific functionality
python3 related_extractor.py

# Verify permissions
ls -la service_account.json
```

## 📊 Monitoring

### Log Files
- `/var/log/google_trends.log` - Main execution log
- `/var/log/google_trends_related.log` - Related data log

### Key Metrics
- Successful data collection rate
- API rate limit warnings
- Google Sheets write success

### Alerts Setup
Consider setting up alerts for:
- Consecutive failed executions
- Rate limit exceeded warnings
- Google Sheets access errors

## 🛡️ Security

### File Permissions
```bash
# Secure service account file
chmod 600 service_account.json

# Executable permissions
chmod +x run.sh tests/*.sh
```

### Best Practices
- Keep `service_account.json` out of version control
- Regular backup of credentials
- Monitor service account usage
- Rotate credentials periodically

## 🔧 Maintenance

### Regular Tasks
1. Monitor log files for errors
2. Check Google Cloud quota usage
3. Verify cron job execution
4. Update Python dependencies

### Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Pull latest changes
git pull origin master
```

---

**Production Checklist**:
- ✅ Service account configured
- ✅ Google Sheets shared
- ✅ Config.py updated
- ✅ Cron jobs scheduled
- ✅ Logging enabled
- ✅ Permissions set
- ✅ Testing completed

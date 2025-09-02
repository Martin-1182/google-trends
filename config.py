# Google Trends Data Monitoring - Configuration
# Edit this file to configure data collection parameters

# Authentication settings
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_NAME = 'Google Trends Monitoring'

# Keywords to track
KEYWORDS = [
    "online marketing",
    "seo", 
    "social media",
    "skincare"
]

# Geographic regions mapping
GEO_MAPPING = {
    'Slovensko': 'SK',
    'Česko': 'CZ',
    'Global': ''  # Empty string for global data
}

# Time frame for data collection
TIMEFRAME = 'today 3-m'  # Last 3 months

# Request settings
REQUEST_DELAY = 60  # Seconds between requests (increased to avoid rate limiting)

# Data collection settings
COLLECT_RELATED_TOPICS = True
COLLECT_RELATED_QUERIES = True

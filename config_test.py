# Test configuration with minimal load
KEYWORDS = ["skincare"]
GEO_MAPPING = {"Slovensko": "SK"}
TIMEFRAME = "today 3-m"
REQUEST_DELAY = 45  # Longer delay for testing
COLLECT_INTEREST_OVER_TIME = True
COLLECT_RELATED_TOPICS = False  # Disabled for testing
COLLECT_RELATED_QUERIES = False  # Disabled for testing
SPREADSHEET_NAME = "Google Trends Monitoring"
SERVICE_ACCOUNT_FILE = "service_account.json"

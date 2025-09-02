# Google Trends Configuration
# Edit this file to configure what data to collect

# Keywords to track (reduced for testing)
KEYWORDS = [
    "online marketing",
    "skincare"
]

# Geographic regions mapping (reduced for testing)
GEO_MAPPING = {
    "Slovensko": "SK",
    "Česko": "CZ"
}

# Time frame for data collection
TIMEFRAME = "today 3-m"

# Delay between requests (increased to avoid rate limiting)
REQUEST_DELAY = 30  # seconds

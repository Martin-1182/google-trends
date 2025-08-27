#!/usr/bin/env python3
"""
Get service account email for sharing spreadsheets
"""
import json
import sys

SERVICE_ACCOUNT_FILE = '/var/www/Google-trends-data/service_account.json'

try:
    with open(SERVICE_ACCOUNT_FILE, 'r') as f:
        data = json.load(f)
        email = data.get('client_email', 'Not found')
        print(f"📧 Service Account Email: {email}")
        print()
        print("🔗 To share a Google Sheet with this service account:")
        print("1. Open your Google Sheet")
        print("2. Click 'Share' button")
        print("3. Paste the email above")
        print("4. Give 'Editor' permissions")
        print("5. Click 'Share'")
except FileNotFoundError:
    print("❌ service_account.json not found!")
    print("Please create it following the setup instructions.")
except json.JSONDecodeError:
    print("❌ Invalid JSON in service_account.json")
except Exception as e:
    print(f"❌ Error: {e}")

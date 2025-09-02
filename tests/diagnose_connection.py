#!/usr/bin/env python3
"""
Comprehensive Google Sheets diagnostic script
"""
import gspread
import json
import sys

SERVICE_ACCOUNT_FILE = '/var/www/Google-trends-data/service_account.json'
GOOGLE_SHEET_NAME = 'Google Trends Monitoring'

def diagnose_connection():
    print("🔍 Google Sheets Connection Diagnostic")
    print("=" * 50)

    # Step 1: Check service account file
    print("1. Checking service account file...")
    try:
        with open(SERVICE_ACCOUNT_FILE, 'r') as f:
            sa_data = json.load(f)
        print("   ✅ Service account file exists and is valid JSON")
        print(f"   📧 Service Account: {sa_data.get('client_email', 'Unknown')}")
        print(f"   🏢 Project ID: {sa_data.get('project_id', 'Unknown')}")
    except FileNotFoundError:
        print("   ❌ Service account file not found!")
        print(f"   Expected at: {SERVICE_ACCOUNT_FILE}")
        return
    except json.JSONDecodeError:
        print("   ❌ Invalid JSON in service account file!")
        return
    except Exception as e:
        print(f"   ❌ Error reading service account file: {e}")
        return

    print()

    # Step 2: Test authentication
    print("2. Testing authentication...")
    try:
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        print("   ✅ Authentication successful")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        print("   💡 Check if Google Drive and Sheets APIs are enabled")
        return

    print()

    # Step 3: List all accessible spreadsheets
    print("3. Listing all accessible spreadsheets...")
    try:
        spreadsheets = gc.list_spreadsheet_files()
        print(f"   📄 Found {len(spreadsheets)} spreadsheet(s):")
        if spreadsheets:
            for i, sheet in enumerate(spreadsheets, 1):
                print(f"   {i}. \"{sheet['name']}\" (ID: {sheet['id']})")
        else:
            print("   ❌ No spreadsheets found!")
    except Exception as e:
        print(f"   ❌ Error listing spreadsheets: {e}")
        return

    print()

    # Step 4: Try to open the target spreadsheet
    print(f"4. Trying to open '{GOOGLE_SHEET_NAME}'...")
    try:
        spreadsheet = gc.open(GOOGLE_SHEET_NAME)
        print("   ✅ Spreadsheet opened successfully!")
        print(f"   🔗 URL: {spreadsheet.url}")

        # Check worksheets
        worksheets = spreadsheet.worksheets()
        print(f"   📋 Found {len(worksheets)} worksheet(s):")
        for ws in worksheets:
            print(f"      - {ws.title} ({ws.row_count}x{ws.col_count})")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"   ❌ Spreadsheet '{GOOGLE_SHEET_NAME}' not found!")
        print("   💡 Troubleshooting steps:")
        print("      - Check the exact name (case sensitive)")
        print("      - Ensure it's shared with the service account")
        print("      - Try refreshing the sharing settings")
        print("      - Wait a few minutes for sharing to propagate")

    except Exception as e:
        print(f"   ❌ Error opening spreadsheet: {e}")

    print()
    print("🎯 Next Steps:")
    if spreadsheets:
        print("   - If you see your spreadsheet above, check the exact name")
        print("   - Update GOOGLE_SHEET_NAME in the script if needed")
    else:
        print("   - Create a Google Sheet named 'Google Trends Monitoring'")
        print("   - Share it with the service account email shown above")
        print("   - Give 'Editor' permissions")

    print()
    print("🔄 Run this diagnostic again after making changes:")
    print("   python3 diagnose_connection.py")

if __name__ == "__main__":
    diagnose_connection()

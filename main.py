#!/usr/bin/env python3
"""
Google Trends Data Collector
Main script for collecting Google Trends data and writing to Google Sheets
"""

import pandas as pd
from pytrends.request import TrendReq
import gspread
from gspread_dataframe import set_with_dataframe
from gspread.exceptions import SpreadsheetNotFound
import time
import json
import sys
import os

# Import configuration
try:
    # Check if we're running from test_minimal
    if 'test_minimal' in ' '.join(sys.argv):
        try:
            from config_test import *
            print("📋 Using test configuration")
        except ImportError:
            from config import *
            print("📋 Using default configuration")
    else:
        from config import *
except ImportError:
    print("❌ Configuration file 'config.py' not found!")
    print("Please create config.py file with your settings.")
    sys.exit(1)


class GoogleTrendsCollector:
    """Main class for collecting Google Trends data"""
    
    def __init__(self):
        self.pytrends = None
        self.spreadsheet = None
        self.gc = None
        
    def initialize_google_sheets(self):
        """Initialize connection to Google Sheets"""
        try:
            self.gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
            print("✅ Google Sheets authentication successful")
            
            try:
                self.spreadsheet = self.gc.open(SPREADSHEET_NAME)
                print(f"✅ Connected to Google Sheet: '{SPREADSHEET_NAME}'")
                return True
                
            except SpreadsheetNotFound:
                print(f"❌ Google Sheet '{SPREADSHEET_NAME}' not found")
                self._show_sheet_setup_help()
                return False
                
        except FileNotFoundError:
            print(f"❌ Service account file '{SERVICE_ACCOUNT_FILE}' not found")
            print("Please add your service_account.json file to the project directory")
            return False
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            return False
    
    def _show_sheet_setup_help(self):
        """Show help for setting up Google Sheet"""
        try:
            with open(SERVICE_ACCOUNT_FILE, 'r') as f:
                data = json.load(f)
                email = data.get('client_email', 'Unknown')
                print(f"\n📧 Service Account Email: {email}")
                print("\n🔗 To create and share Google Sheet:")
                print("1. Create new Google Sheet named exactly:", SPREADSHEET_NAME)
                print("2. Share it with the email above")
                print("3. Give 'Editor' permissions")
        except:
            print("\n❌ Could not read service account email")
    
    def initialize_pytrends(self):
        """Initialize pytrends connection"""
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360)
            print("✅ Google Trends connection initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Google Trends: {e}")
            return False
    
    def get_interest_over_time(self, keyword, geo_code):
        """Get Interest Over Time data"""
        try:
            self.pytrends.build_payload([keyword], cat=0, timeframe=TIMEFRAME, geo=geo_code, gprop='')
            df = self.pytrends.interest_over_time()
            
            if not df.empty:
                if 'isPartial' in df.columns:
                    df = df.drop(columns=['isPartial'])
                df.reset_index(inplace=True)
                df.rename(columns={'date': 'Date'}, inplace=True)
                return df
            return pd.DataFrame()
            
        except Exception as e:
            print(f"    ❌ Interest Over Time error: {e}")
            return pd.DataFrame()
    
    def get_related_topics(self, keyword, geo_code):
        """Get Related Topics data"""
        try:
            related_topics = self.pytrends.related_topics()
            
            if not related_topics or keyword not in related_topics:
                return pd.DataFrame()
            
            data = related_topics[keyword]
            dfs = []
            
            # Top topics
            if data['top'] is not None and not data['top'].empty:
                top_df = data['top'].copy()
                top_df['Type'] = 'Top'
                top_df['Keyword'] = keyword
                dfs.append(top_df)
            
            # Rising topics
            if data['rising'] is not None and not data['rising'].empty:
                rising_df = data['rising'].copy()
                rising_df['Type'] = 'Rising'
                rising_df['Keyword'] = keyword
                dfs.append(rising_df)
            
            if dfs:
                return pd.concat(dfs, ignore_index=True)
            return pd.DataFrame()
            
        except Exception as e:
            print(f"    ❌ Related Topics error: {e}")
            return pd.DataFrame()
    
    def get_related_queries(self, keyword, geo_code):
        """Get Related Queries data"""
        try:
            related_queries = self.pytrends.related_queries()
            
            if not related_queries or keyword not in related_queries:
                return pd.DataFrame()
            
            data = related_queries[keyword]
            dfs = []
            
            # Top queries
            if data['top'] is not None and not data['top'].empty:
                top_df = data['top'].copy()
                top_df['Type'] = 'Top'
                top_df['Keyword'] = keyword
                dfs.append(top_df)
            
            # Rising queries
            if data['rising'] is not None and not data['rising'].empty:
                rising_df = data['rising'].copy()
                rising_df['Type'] = 'Rising'
                rising_df['Keyword'] = keyword
                dfs.append(rising_df)
            
            if dfs:
                return pd.concat(dfs, ignore_index=True)
            return pd.DataFrame()
            
        except Exception as e:
            print(f"    ❌ Related Queries error: {e}")
            return pd.DataFrame()
    
    def write_to_sheet(self, df, tab_name):
        """Write DataFrame to Google Sheet tab"""
        if df.empty:
            return False
            
        try:
            try:
                worksheet = self.spreadsheet.worksheet(tab_name)
                print(f"    📄 Tab '{tab_name}' found, clearing old data")
            except gspread.WorksheetNotFound:
                print(f"    📄 Creating new tab '{tab_name}'")
                worksheet = self.spreadsheet.add_worksheet(title=tab_name, rows=max(200, len(df) + 10), cols=20)
            
            worksheet.clear()
            set_with_dataframe(worksheet, df)
            print(f"    ✅ Written {len(df)} rows to '{tab_name}'")
            return True
            
        except Exception as e:
            print(f"    ❌ Failed to write to '{tab_name}': {e}")
            return False
    
    def collect_data_for_keyword(self, keyword, country_name, geo_code):
        """Collect all data for a specific keyword and country"""
        print(f"\n🔍 Processing: {keyword} ({country_name})")
        
        success_count = 0
        
        # 1. Interest Over Time
        if COLLECT_INTEREST_OVER_TIME:
            print("  📈 Collecting Interest Over Time...")
            df = self.get_interest_over_time(keyword, geo_code)
            if not df.empty:
                tab_name = f"{country_name}_{keyword}_Interest"
                if self.write_to_sheet(df, tab_name):
                    success_count += 1
        
        # Small delay between different data types
        time.sleep(2)
        
        # 2. Related Topics
        if COLLECT_RELATED_TOPICS:
            print("  🏷️  Collecting Related Topics...")
            df = self.get_related_topics(keyword, geo_code)
            if not df.empty:
                tab_name = f"{country_name}_{keyword}_Topics"
                if self.write_to_sheet(df, tab_name):
                    success_count += 1
        
        time.sleep(2)
        
        # 3. Related Queries
        if COLLECT_RELATED_QUERIES:
            print("  🔍 Collecting Related Queries...")
            df = self.get_related_queries(keyword, geo_code)
            if not df.empty:
                tab_name = f"{country_name}_{keyword}_Queries"
                if self.write_to_sheet(df, tab_name):
                    success_count += 1
        
        return success_count
    
    def run(self):
        """Main execution method"""
        print("🚀 Google Trends Data Collector")
        print("=" * 40)
        
        # Initialize connections
        if not self.initialize_google_sheets():
            return False
            
        if not self.initialize_pytrends():
            return False
        
        print(f"\n📊 Configuration:")
        print(f"  Keywords: {', '.join(KEYWORDS)}")
        print(f"  Countries: {', '.join(GEO_MAPPING.keys())}")
        print(f"  Timeframe: {TIMEFRAME}")
        print(f"  Request delay: {REQUEST_DELAY}s")
        
        total_success = 0
        total_attempts = 0
        
        # Process each country
        for country_name, geo_code in GEO_MAPPING.items():
            print(f"\n🌍 Processing country: {country_name} ({geo_code})")
            
            # Process each keyword
            for keyword in KEYWORDS:
                try:
                    success = self.collect_data_for_keyword(keyword, country_name, geo_code)
                    total_success += success
                    total_attempts += 1
                    
                    # Rate limiting delay
                    if keyword != KEYWORDS[-1] or country_name != list(GEO_MAPPING.keys())[-1]:
                        print(f"  ⏳ Waiting {REQUEST_DELAY}s to avoid rate limiting...")
                        time.sleep(REQUEST_DELAY)
                        
                except Exception as e:
                    print(f"  ❌ Failed to process '{keyword}': {e}")
                    total_attempts += 1
        
        print(f"\n✅ Collection completed!")
        print(f"📊 Success rate: {total_success}/{total_attempts * 3} data sets collected")
        print(f"🔗 Google Sheet: {self.spreadsheet.url if self.spreadsheet else 'N/A'}")
        
        return True


def main():
    """Main function"""
    collector = GoogleTrendsCollector()
    success = collector.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

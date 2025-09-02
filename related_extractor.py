#!/usr/bin/env python3
"""
Google Trends Related Topics and Queries Extractor
Single script to extract Related Topics and Related Queries based on keywords, geo, and timeframe
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pytrends.request import TrendReq
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import json
import time
from datetime import datetime

class GoogleTrendsRelatedExtractor:
    """Extract Related Topics and Queries from Google Trends"""
    
    def __init__(self, hl='en-US', tz=360):
        """Initialize the extractor"""
        self.hl = hl
        self.tz = tz
        self.pytrends = None
        self.gc = None
        self.spreadsheet = None
        
    def initialize(self):
        """Initialize Google Trends and Google Sheets connections"""
        try:
            # Initialize pytrends
            self.pytrends = TrendReq(hl=self.hl, tz=self.tz)
            print("✅ Google Trends connection initialized")
            
            # Initialize Google Sheets
            try:
                import config
                self.gc = gspread.service_account(filename=config.SERVICE_ACCOUNT_FILE)
                self.spreadsheet = self.gc.open(config.SPREADSHEET_NAME)
                print(f"✅ Connected to Google Sheet: '{config.SPREADSHEET_NAME}'")
                return True
            except Exception as e:
                print(f"❌ Google Sheets connection failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def extract_related_data(self, keywords, geo_mapping, timeframe='today 3-m', delay=30):
        """
        Extract Related Topics and Queries for given parameters
        
        Args:
            keywords (list): List of keywords to analyze
            geo_mapping (dict): Dictionary mapping country names to geo codes
            timeframe (str): Time period (e.g., 'today 3-m')
            delay (int): Delay between requests in seconds
        
        Returns:
            dict: Results with related topics and queries data
        """
        results = {
            'related_topics': [],
            'related_queries': [],
            'success_count': 0,
            'total_requests': 0
        }
        
        print(f"\n🚀 Google Trends Related Data Extractor")
        print("=" * 50)
        print(f"📊 Configuration:")
        print(f"  Keywords: {', '.join(keywords)}")
        print(f"  Countries: {', '.join(geo_mapping.keys())}")
        print(f"  Timeframe: {timeframe}")
        print(f"  Request delay: {delay}s")
        
        for country_name, geo_code in geo_mapping.items():
            print(f"\n🌍 Processing country: {country_name} ({geo_code})")
            
            for keyword in keywords:
                print(f"\n🔍 Processing: {keyword} ({country_name})")
                results['total_requests'] += 1
                
                try:
                    # Build payload
                    self.pytrends.build_payload(
                        kw_list=[keyword],
                        cat=0,
                        timeframe=timeframe,
                        geo=geo_code,
                        gprop=''
                    )
                    
                    # Extract Related Topics
                    topics_data = self._extract_related_topics(keyword, country_name, geo_code)
                    if topics_data is not None and not topics_data.empty:
                        results['related_topics'].append(topics_data)
                        print(f"  ✅ Related Topics: {len(topics_data)} items")
                        results['success_count'] += 1
                    else:
                        print(f"  ⚠️ No Related Topics data")
                    
                    # Extract Related Queries
                    queries_data = self._extract_related_queries(keyword, country_name, geo_code)
                    if queries_data is not None and not queries_data.empty:
                        results['related_queries'].append(queries_data)
                        print(f"  ✅ Related Queries: {len(queries_data)} items")
                        results['success_count'] += 1
                    else:
                        print(f"  ⚠️ No Related Queries data")
                    
                except Exception as e:
                    print(f"  ❌ Error processing {keyword}: {e}")
                
                # Rate limiting delay
                if delay > 0:
                    print(f"  ⏳ Waiting {delay}s to avoid rate limiting...")
                    time.sleep(delay)
        
        return results
    
    def _extract_related_topics(self, keyword, country_name, geo_code):
        """Extract Related Topics using official pytrends API"""
        try:
            # Use official pytrends related_topics() method
            related_topics = self.pytrends.related_topics()
            
            if not related_topics or keyword not in related_topics:
                print(f"    📝 No related topics data for '{keyword}'")
                return None
            
            data = related_topics[keyword]
            dfs = []
            
            # Process top topics
            if 'top' in data and data['top'] is not None and not data['top'].empty:
                top_df = data['top'].copy()
                top_df['Type'] = 'Top'
                top_df['Keyword'] = keyword
                top_df['Country'] = country_name
                top_df['Geo_Code'] = geo_code
                top_df['Extracted_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dfs.append(top_df)
                print(f"    📊 Top topics: {len(top_df)} items")
            
            # Process rising topics
            if 'rising' in data and data['rising'] is not None and not data['rising'].empty:
                rising_df = data['rising'].copy()
                rising_df['Type'] = 'Rising'
                rising_df['Keyword'] = keyword
                rising_df['Country'] = country_name
                rising_df['Geo_Code'] = geo_code
                rising_df['Extracted_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dfs.append(rising_df)
                print(f"    📈 Rising topics: {len(rising_df)} items")
            
            if dfs:
                return pd.concat(dfs, ignore_index=True)
            return None
            
        except Exception as e:
            print(f"    ❌ Related Topics error: {e}")
            return None
    
    def _extract_related_queries(self, keyword, country_name, geo_code):
        """Extract Related Queries using official pytrends API"""
        try:
            # Use official pytrends related_queries() method
            related_queries = self.pytrends.related_queries()
            
            if not related_queries or keyword not in related_queries:
                print(f"    📝 No related queries data for '{keyword}'")
                return None
            
            data = related_queries[keyword]
            dfs = []
            
            # Process top queries
            if 'top' in data and data['top'] is not None and not data['top'].empty:
                top_df = data['top'].copy()
                top_df['Type'] = 'Top'
                top_df['Keyword'] = keyword
                top_df['Country'] = country_name
                top_df['Geo_Code'] = geo_code
                top_df['Extracted_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dfs.append(top_df)
                print(f"    📊 Top queries: {len(top_df)} items")
            
            # Process rising queries
            if 'rising' in data and data['rising'] is not None and not data['rising'].empty:
                rising_df = data['rising'].copy()
                rising_df['Type'] = 'Rising'
                rising_df['Keyword'] = keyword
                rising_df['Country'] = country_name
                rising_df['Geo_Code'] = geo_code
                rising_df['Extracted_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dfs.append(rising_df)
                print(f"    📈 Rising queries: {len(rising_df)} items")
            
            if dfs:
                return pd.concat(dfs, ignore_index=True)
            return None
            
        except Exception as e:
            print(f"    ❌ Related Queries error: {e}")
            return None
    
    def save_to_sheets(self, results):
        """Save results to Google Sheets"""
        if not self.spreadsheet:
            print("❌ Google Sheets not initialized")
            return False
        
        saved_count = 0
        
        # Save Related Topics
        if results['related_topics']:
            topics_df = pd.concat(results['related_topics'], ignore_index=True)
            if self._write_to_sheet(topics_df, "Related Topics"):
                saved_count += 1
        
        # Save Related Queries
        if results['related_queries']:
            queries_df = pd.concat(results['related_queries'], ignore_index=True)
            if self._write_to_sheet(queries_df, "Related Queries"):
                saved_count += 1
        
        return saved_count > 0
        """Write DataFrame to Google Sheet tab"""
        if df.empty:
            return False
            
        try:
            try:
                worksheet = self.spreadsheet.worksheet(tab_name)
                print(f"📄 Tab '{tab_name}' found, clearing old data")
            except gspread.WorksheetNotFound:
                print(f"📄 Creating new tab '{tab_name}'")
                worksheet = self.spreadsheet.add_worksheet(title=tab_name, rows=max(200, len(df) + 10), cols=20)
            
            worksheet.clear()
            set_with_dataframe(worksheet, df)
            print(f"✅ Written {len(df)} rows to '{tab_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Failed to write to '{tab_name}': {e}")
            return False

def main():
    """Main function to extract related data"""
    try:
        # Load configuration
        import config
        
        # Initialize extractor
        extractor = GoogleTrendsRelatedExtractor(hl='sk-SK', tz=60)
        
        if not extractor.initialize():
            print("❌ Failed to initialize extractor")
            return
        
        # Extract related data
        results = extractor.extract_related_data(
            keywords=config.KEYWORDS,
            geo_mapping=config.GEO_MAPPING,
            timeframe=config.TIMEFRAME,
            delay=config.REQUEST_DELAY
        )
        
        # Print summary
        print(f"\n📊 Extraction Summary:")
        print(f"  Total requests: {results['total_requests']}")
        print(f"  Successful extractions: {results['success_count']}")
        print(f"  Related Topics datasets: {len(results['related_topics'])}")
        print(f"  Related Queries datasets: {len(results['related_queries'])}")
        
        # Save to Google Sheets
        if results['related_topics'] or results['related_queries']:
            print(f"\n💾 Saving to Google Sheets...")
            if extractor.save_to_sheets(results):
                print(f"✅ Data saved successfully!")
                print(f"🔗 Google Sheet: https://docs.google.com/spreadsheets/d/{extractor.spreadsheet.id}")
            else:
                print(f"❌ Failed to save data")
        else:
            print(f"\n⚠️ No data to save")
        
        print(f"\n✅ Related data extraction completed!")
        
    except Exception as e:
        print(f"❌ Main error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

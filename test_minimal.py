#!/usr/bin/env python3
"""
Simple test of the Google Trends collector with minimal configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import test configuration
import config_test as config

from main import GoogleTrendsCollector

def main():
    print("🧪 Testing Google Trends Collector with minimal configuration...")
    print(f"Keywords: {config.KEYWORDS}")
    print(f"Countries: {list(config.GEO_MAPPING.keys())}")
    print(f"Delay: {config.REQUEST_DELAY}s")
    print("-" * 50)
    
    try:
        collector = GoogleTrendsCollector()
        collector.run()
        print("✅ Test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()

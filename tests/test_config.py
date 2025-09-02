#!/usr/bin/env python3
"""
Configuration validator and test runner
"""

import sys
import os
sys.path.append('..')

def test_config():
    """Test configuration file"""
    try:
        import config
        print("✅ Configuration loaded successfully")
        
        print(f"📊 Keywords: {len(config.KEYWORDS)} items")
        for i, keyword in enumerate(config.KEYWORDS, 1):
            print(f"  {i}. {keyword}")
        
        print(f"🌍 Countries: {len(config.GEO_MAPPING)} items")
        for name, code in config.GEO_MAPPING.items():
            print(f"  {name}: {code}")
        
        print(f"⏰ Timeframe: {config.TIMEFRAME}")
        print(f"📋 Sheet name: {config.GOOGLE_SHEET_NAME}")
        print(f"🔧 Service account: {config.SERVICE_ACCOUNT_FILE}")
        
        # Check data collection settings
        print(f"📈 Collect Interest Over Time: {config.COLLECT_INTEREST_OVER_TIME}")
        print(f"🏷️  Collect Related Topics: {config.COLLECT_RELATED_TOPICS}")
        print(f"🔍 Collect Related Queries: {config.COLLECT_RELATED_QUERIES}")
        print(f"⏳ Request delay: {config.REQUEST_DELAY}s")
        
        return True
        
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_service_account():
    """Test service account file"""
    try:
        import config
        
        if not os.path.exists(f"../{config.SERVICE_ACCOUNT_FILE}"):
            print(f"❌ Service account file not found: {config.SERVICE_ACCOUNT_FILE}")
            return False
        
        import json
        with open(f"../{config.SERVICE_ACCOUNT_FILE}", 'r') as f:
            data = json.load(f)
        
        email = data.get('client_email', 'Unknown')
        project = data.get('project_id', 'Unknown')
        
        print(f"✅ Service account file valid")
        print(f"📧 Email: {email}")
        print(f"🏢 Project: {project}")
        
        return True
        
    except Exception as e:
        print(f"❌ Service account test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Google Trends Collector Configuration")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing configuration...")
    if not test_config():
        success = False
    
    print("\n2. Testing service account...")
    if not test_service_account():
        success = False
    
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    return success

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script pre Related Topics a Related Queries
"""

import pandas as pd
from pytrends.request import TrendReq
import json
import time

def test_related_data():
    print("🔍 Testovanie Related Topics a Related Queries")
    print("=" * 50)
    
    # Konfigurácia
    keyword = "duchon"
    geo_code = "SK"
    timeframe = "today 3-m"
    
    print(f"Kľúčové slovo: {keyword}")
    print(f"Krajina: {geo_code}")
    print(f"Časové obdobie: {timeframe}")
    print()
    
    try:
        # Inicializácia pytrends
        pytrends = TrendReq(hl='sk-SK', tz=360)
        
        # Počkáme chvíľu pred začiatkom
        print("⏳ Čakám 5 sekúnd pred začiatkom...")
        time.sleep(5)
        
        # Vytvorenie požiadavky
        print("📡 Vytváram požiadavku na Google Trends...")
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo_code, gprop='')
        
        # 1. Interest Over Time
        print("\n📈 Interest Over Time:")
        interest_df = pytrends.interest_over_time()
        if not interest_df.empty:
            print(f"   ✅ Získané dáta: {len(interest_df)} riadkov")
            print(f"   📊 Stĺpce: {list(interest_df.columns)}")
            print(f"   📅 Od: {interest_df.index.min()} Do: {interest_df.index.max()}")
        else:
            print("   ❌ Žiadne dáta")
        
        # 2. Related Topics
        print("\n🏷️  Related Topics:")
        related_topics = pytrends.related_topics()
        
        if related_topics and keyword in related_topics:
            topics_data = related_topics[keyword]
            
            # Top topics
            if topics_data['top'] is not None and not topics_data['top'].empty:
                print(f"   ✅ Top Topics: {len(topics_data['top'])} záznamov")
                print("   📋 Ukážka Top Topics:")
                print(topics_data['top'].head().to_string(index=False))
            else:
                print("   ❌ Žiadne Top Topics")
            
            print()
            
            # Rising topics
            if topics_data['rising'] is not None and not topics_data['rising'].empty:
                print(f"   ✅ Rising Topics: {len(topics_data['rising'])} záznamov")
                print("   📋 Ukážka Rising Topics:")
                print(topics_data['rising'].head().to_string(index=False))
            else:
                print("   ❌ Žiadne Rising Topics")
        else:
            print("   ❌ Žiadne Related Topics")
        
        # 3. Related Queries
        print("\n🔍 Related Queries:")
        related_queries = pytrends.related_queries()
        
        if related_queries and keyword in related_queries:
            queries_data = related_queries[keyword]
            
            # Top queries
            if queries_data['top'] is not None and not queries_data['top'].empty:
                print(f"   ✅ Top Queries: {len(queries_data['top'])} záznamov")
                print("   📋 Ukážka Top Queries:")
                print(queries_data['top'].head().to_string(index=False))
            else:
                print("   ❌ Žiadne Top Queries")
            
            print()
            
            # Rising queries
            if queries_data['rising'] is not None and not queries_data['rising'].empty:
                print(f"   ✅ Rising Queries: {len(queries_data['rising'])} záznamov")
                print("   📋 Ukážka Rising Queries:")
                print(queries_data['rising'].head().to_string(index=False))
            else:
                print("   ❌ Žiadne Rising Queries")
        else:
            print("   ❌ Žiadne Related Queries")
            
    except Exception as e:
        print(f"❌ Chyba: {e}")
    
    print("\n🎯 Test dokončený!")


if __name__ == "__main__":
    test_related_data()

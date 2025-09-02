#!/usr/bin/env python3
"""
Demo script showing structure of Related Topics and Related Queries
"""

import pandas as pd

def demo_related_data_structure():
    print("📋 Štruktúra Related Topics a Related Queries dát")
    print("=" * 55)
    print()
    
    print("🏷️  RELATED TOPICS štruktúra:")
    print("-" * 30)
    
    # Ukážka Related Topics (Top)
    topics_top_data = {
        'topic_mid': ['/m/0k2wl', '/m/0k5c2', '/m/0k8x1'],
        'topic_title': ['Duchon & spol.', 'Duchon obchodník', 'Duchon firma'],
        'topic_type': ['Business', 'Person', 'Company'],
        'value': [100, 85, 70],
        'formattedValue': ['100', '85', '70'],
        'link': ['https://trends.google.com/...', 'https://trends.google.com/...', 'https://trends.google.com/...']
    }
    
    topics_top_df = pd.DataFrame(topics_top_data)
    topics_top_df['Type'] = 'Top'
    topics_top_df['Keyword'] = 'duchon'
    
    print("📊 Top Topics:")
    print(topics_top_df.to_string(index=False))
    print()
    
    # Ukážka Related Topics (Rising)
    topics_rising_data = {
        'topic_mid': ['/m/0k9x2', '/m/0k1y3'],
        'topic_title': ['Duchon nákup', 'Duchon predaj'],
        'topic_type': ['Activity', 'Activity'],
        'value': [150, 120],
        'formattedValue': ['+150%', '+120%'],
        'link': ['https://trends.google.com/...', 'https://trends.google.com/...']
    }
    
    topics_rising_df = pd.DataFrame(topics_rising_data)
    topics_rising_df['Type'] = 'Rising'
    topics_rising_df['Keyword'] = 'duchon'
    
    print("📈 Rising Topics:")
    print(topics_rising_df.to_string(index=False))
    print()
    
    print("🔍 RELATED QUERIES štruktúra:")
    print("-" * 30)
    
    # Ukážka Related Queries (Top)
    queries_top_data = {
        'query': ['duchon obchod', 'duchon predajňa', 'duchon bratislava'],
        'value': [100, 75, 60],
        'formattedValue': ['100', '75', '60']
    }
    
    queries_top_df = pd.DataFrame(queries_top_data)
    queries_top_df['Type'] = 'Top'
    queries_top_df['Keyword'] = 'duchon'
    
    print("📊 Top Queries:")
    print(queries_top_df.to_string(index=False))
    print()
    
    # Ukážka Related Queries (Rising)
    queries_rising_data = {
        'query': ['duchon leták', 'duchon akcia'],
        'value': [200, 180],
        'formattedValue': ['+200%', '+180%']
    }
    
    queries_rising_df = pd.DataFrame(queries_rising_data)
    queries_rising_df['Type'] = 'Rising'
    queries_rising_df['Keyword'] = 'duchon'
    
    print("📈 Rising Queries:")
    print(queries_rising_df.to_string(index=False))
    print()
    
    print("📋 VÝSLEDNÉ GOOGLE SHEETS TABY:")
    print("-" * 35)
    print("Pre kľúčové slovo 'duchon' v krajine 'Slovensko' sa vytvoria:")
    print("1. 📈 Slovensko_duchon_Interest  - Interest Over Time dáta")
    print("2. 🏷️  Slovensko_duchon_Topics   - Related Topics (Top + Rising)")
    print("3. 🔍 Slovensko_duchon_Queries  - Related Queries (Top + Rising)")
    print()
    
    print("🎯 Každý tab bude mať:")
    print("- Topics: topic_title, topic_type, value, formattedValue, Type, Keyword")
    print("- Queries: query, value, formattedValue, Type, Keyword")
    print("- Interest: Date, duchon (hodnoty 0-100)")


if __name__ == "__main__":
    demo_related_data_structure()

import pandas as pd
from pytrends.request import TrendReq
import gspread
from gspread_dataframe import set_with_dataframe
from gspread.exceptions import SpreadsheetNotFound
import time

# --- KONFIGURÁCIA ---
# Zadajte kľúčové slová, ktoré chcete sledovať
KEYWORDS = ["online marketing"]

# Mapovanie krajín na názvy tabov v Google Sheete
# Formát: 'Názov tabu': 'Kód krajiny'
GEO_MAPPING = {
    'Slovensko': 'SK',
    'Česko': 'CZ'
}

# Časové obdobie (viac info: https://github.com/GeneralMills/pytrends)
TIMEFRAME = 'today 3-m'  # Posledných 90 dní

# Cesta k JSON súboru so Service Account kľúčmi
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Názov Google Sheet dokumentu, do ktorého sa budú dáta zapisovať
GOOGLE_SHEET_NAME = 'Google Trends Monitoring'
# --- KONIEC KONFIGURÁCIE ---


def get_related_data(pytrends, keyword, geo_code):
    """
    Získa Related Topics a Related Queries pre dané kľúčové slovo.
    """
    try:
        # Vytvorenie požiadavky na Google Trends
        pytrends.build_payload([keyword], cat=0, timeframe=TIMEFRAME, geo=geo_code, gprop='')
        
        # Získanie Related Topics
        related_topics = pytrends.related_topics()
        
        # Získanie Related Queries
        related_queries = pytrends.related_queries()
        
        return related_topics, related_queries
    
    except Exception as e:
        print(f"Chyba pri získavaní related dát pre '{keyword}': {e}")
        return None, None


def process_related_topics(related_topics, keyword):
    """
    Spracuje Related Topics data do DataFrame.
    """
    if not related_topics or keyword not in related_topics:
        return pd.DataFrame()
    
    data = related_topics[keyword]
    
    # Rising topics
    rising_df = pd.DataFrame()
    if data['rising'] is not None and not data['rising'].empty:
        rising_df = data['rising'].copy()
        rising_df['Type'] = 'Rising'
        rising_df['Keyword'] = keyword
    
    # Top topics
    top_df = pd.DataFrame()
    if data['top'] is not None and not data['top'].empty:
        top_df = data['top'].copy()
        top_df['Type'] = 'Top'
        top_df['Keyword'] = keyword
    
    # Kombinovanie oboch dataframov
    if not rising_df.empty and not top_df.empty:
        combined_df = pd.concat([top_df, rising_df], ignore_index=True)
    elif not rising_df.empty:
        combined_df = rising_df
    elif not top_df.empty:
        combined_df = top_df
    else:
        combined_df = pd.DataFrame()
    
    return combined_df


def process_related_queries(related_queries, keyword):
    """
    Spracuje Related Queries data do DataFrame.
    """
    if not related_queries or keyword not in related_queries:
        return pd.DataFrame()
    
    data = related_queries[keyword]
    
    # Rising queries
    rising_df = pd.DataFrame()
    if data['rising'] is not None and not data['rising'].empty:
        rising_df = data['rising'].copy()
        rising_df['Type'] = 'Rising'
        rising_df['Keyword'] = keyword
    
    # Top queries
    top_df = pd.DataFrame()
    if data['top'] is not None and not data['top'].empty:
        top_df = data['top'].copy()
        top_df['Type'] = 'Top'
        top_df['Keyword'] = keyword
    
    # Kombinovanie oboch dataframov
    if not rising_df.empty and not top_df.empty:
        combined_df = pd.concat([top_df, rising_df], ignore_index=True)
    elif not rising_df.empty:
        combined_df = rising_df
    elif not top_df.empty:
        combined_df = top_df
    else:
        combined_df = pd.DataFrame()
    
    return combined_df


def update_trends_data():
    """
    Hlavná funkcia, ktorá stiahne dáta z Trends a zapíše ich do Google Sheets.
    """
    print("Spúšťam aktualizáciu Google Trends dát...")

    # Pripojenie ku Google Sheets
    try:
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        print("Service account authentication successful")

        # Try to open existing spreadsheet
        try:
            spreadsheet = gc.open(GOOGLE_SHEET_NAME)
            print(f"Úspešne pripojený k Google Sheetu: '{GOOGLE_SHEET_NAME}'")
        except SpreadsheetNotFound:
            print(f"Google Sheet '{GOOGLE_SHEET_NAME}' nebol nájdený.")
            print("Možnosti:")
            print("1. Vytvorte Google Sheet manuálne s názvom '{GOOGLE_SHEET_NAME}'")
            print("2. Zdieľajte existujúci sheet s service account emailom")
            print("3. Alebo upravte názov v konfigurácii")
            print()
            print("Service account email z vášho JSON súboru:")
            try:
                import json
                with open(SERVICE_ACCOUNT_FILE, 'r') as f:
                    data = json.load(f)
                    print(f"📧 {data['client_email']}")
            except:
                print("📧 (skontrolujte 'client_email' vo vašom service_account.json)")
            return

        except Exception as sheet_error:
            if "storage quota" in str(sheet_error).lower():
                print("❌ Google Drive storage quota exceeded!")
                print("Riešenia:")
                print("1. Vytvorte Google Sheet manuálne")
                print("2. Zdieľajte existujúci sheet s service accountom")
                print("3. Vyčistite Google Drive service accountu")
                print()
                print("Service account email:")
                try:
                    import json
                    with open(SERVICE_ACCOUNT_FILE, 'r') as f:
                        data = json.load(f)
                        print(f"📧 {data['client_email']}")
                except:
                    print("📧 (skontrolujte vo vašom service_account.json)")
                return
            else:
                print(f"Chyba pri otváraní Google Sheetu: {sheet_error}")
                return

    except FileNotFoundError:
        print(f"Súbor {SERVICE_ACCOUNT_FILE} nebol nájdený.")
        print("Prosím, vytvorte service_account.json súbor podľa návodu v README.md")
        return
    except Exception as e:
        print(f"Chyba pri pripájaní ku Google Sheets: {e}")
        print("Možné príčiny:")
        print("- Neplatné service account credentials")
        print("- Problém s internetovým pripojením")
        print("- Google API nie je povolené")
        return

    # Inicializácia pripojenia ku Google Trends
    pytrends = TrendReq(hl='en-US', tz=360)

    # Prechádzanie všetkých nakonfigurovaných krajín
    for sheet_name, geo_code in GEO_MAPPING.items():
        print(f"\nSpracovávam krajinu: {sheet_name} ({geo_code})")
        
        # Pre každé kľúčové slovo
        for keyword in KEYWORDS:
            print(f"  Spracovávam kľúčové slovo: '{keyword}'")
            
            try:
                # 1. Získanie Interest Over Time
                pytrends.build_payload([keyword], cat=0, timeframe=TIMEFRAME, geo=geo_code, gprop='')
                interest_df = pytrends.interest_over_time()
                
                if not interest_df.empty:
                    # Odstránenie stĺpca 'isPartial'
                    if 'isPartial' in interest_df.columns:
                        interest_df = interest_df.drop(columns=['isPartial'])
                    
                    # Reset indexu
                    interest_df.reset_index(inplace=True)
                    interest_df.rename(columns={'date': 'Date'}, inplace=True)
                    
                    # Zápis Interest Over Time
                    tab_name = f"{sheet_name}_{keyword}_Interest"
                    try:
                        worksheet = spreadsheet.worksheet(tab_name)
                        print(f"    Tab '{tab_name}' nájdený. Čistím staré dáta.")
                    except gspread.WorksheetNotFound:
                        print(f"    Tab '{tab_name}' neexistuje. Vytváram nový.")
                        worksheet = spreadsheet.add_worksheet(title=tab_name, rows="200", cols="20")
                    
                    worksheet.clear()
                    set_with_dataframe(worksheet, interest_df)
                    print(f"    Interest Over Time dáta zapísané ({len(interest_df)} riadkov)")
                
                # 2. Získanie Related Topics a Queries
                related_topics, related_queries = get_related_data(pytrends, keyword, geo_code)
                
                # 3. Spracovanie Related Topics
                if related_topics:
                    topics_df = process_related_topics(related_topics, keyword)
                    if not topics_df.empty:
                        tab_name = f"{sheet_name}_{keyword}_Topics"
                        try:
                            worksheet = spreadsheet.worksheet(tab_name)
                            print(f"    Tab '{tab_name}' nájdený. Čistím staré dáta.")
                        except gspread.WorksheetNotFound:
                            print(f"    Tab '{tab_name}' neexistuje. Vytváram nový.")
                            worksheet = spreadsheet.add_worksheet(title=tab_name, rows="200", cols="20")
                        
                        worksheet.clear()
                        set_with_dataframe(worksheet, topics_df)
                        print(f"    Related Topics zapísané ({len(topics_df)} riadkov)")
                
                # 4. Spracovanie Related Queries
                if related_queries:
                    queries_df = process_related_queries(related_queries, keyword)
                    if not queries_df.empty:
                        tab_name = f"{sheet_name}_{keyword}_Queries"
                        try:
                            worksheet = spreadsheet.worksheet(tab_name)
                            print(f"    Tab '{tab_name}' nájdený. Čistím staré dáta.")
                        except gspread.WorksheetNotFound:
                            print(f"    Tab '{tab_name}' neexistuje. Vytváram nový.")
                            worksheet = spreadsheet.add_worksheet(title=tab_name, rows="200", cols="20")
                        
                        worksheet.clear()
                        set_with_dataframe(worksheet, queries_df)
                        print(f"    Related Queries zapísané ({len(queries_df)} riadkov)")

            except Exception as e:
                print(f"    Nastala chyba pri spracovaní '{keyword}': {e}")
            
            # Pauza medzi požiadavkami
            print("    Čakám 10 sekúnd pred ďalšou požiadavkou...")
            time.sleep(10)

    print("\nAktualizácia dokončená.")


if __name__ == "__main__":
    update_trends_data()

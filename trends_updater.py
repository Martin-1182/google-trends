import pandas as pd
from pytrends.request import TrendReq
import gspread
from gspread_dataframe import set_with_dataframe
from gspread.exceptions import SpreadsheetNotFound
import time

# --- KONFIGURÁCIA ---
# Zadajte kľúčové slová, ktoré chcete sledovať
KEYWORDS = ["skincare", "cosrx", "kórejska kozmetika", "Beauty Of Joseon"]

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
        print(f"\nSpracovávam: {sheet_name} ({geo_code})")
        
        try:
            # Vytvorenie požiadavky na Google Trends
            pytrends.build_payload(KEYWORDS, cat=0, timeframe=TIMEFRAME, geo=geo_code, gprop='')
            
            # Získanie dát "Interest Over Time"
            df = pytrends.interest_over_time()

            if df.empty:
                print(f"Pre {sheet_name} neboli vrátené žiadne dáta. Preskakujem.")
                continue

            # Odstránenie stĺpca 'isPartial', ktorý indikuje nekompletné dáta
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            
            # Reset indexu, aby sa dátum stal bežným stĺpcom
            df.reset_index(inplace=True)
            # Premenovanie stĺpca 'date' na 'Date' pre krajší vzhľad
            df.rename(columns={'date': 'Date'}, inplace=True)

            print(f"Dáta úspešne stiahnuté. Počet riadkov: {len(df)}")

            # Pripojenie ku konkrétnemu tabu (worksheetu)
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
                print(f"Tab '{sheet_name}' nájdený. Čistím staré dáta.")
            except gspread.WorksheetNotFound:
                print(f"Tab '{sheet_name}' neexistuje. Vytváram nový.")
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
            
            worksheet.clear()
            
            # Zápis dát (DataFrame) do tabu
            set_with_dataframe(worksheet, df)
            
            print(f"Dáta pre '{sheet_name}' boli úspešne zapísané.")

        except Exception as e:
            # Vypísanie chybovej hlášky, ak niečo zlyhá (napr. rate limiting)
            print(f"Nastala chyba pri spracovaní '{sheet_name}': {e}")
        
        # Slušná pauza medzi požiadavkami, aby sme predišli rate limitingu
        print("Čakám 10 sekúnd pred ďalšou požiadavkou...")
        time.sleep(10)

    print("\nAktualizácia dokončená.")


if __name__ == "__main__":
    update_trends_data()

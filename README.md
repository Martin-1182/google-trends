# Automatizácia Google Trends pomocou Pythonu

## Cieľ

Automaticky sťahovať dáta z Google Trends a zapisovať ich do Google Sheets. Skript bude bežať na privátnom serveri.

## Technologický balíček (Stack)

- **Jazyk:** Python 3
- **Google Trends:** Knižnica pytrends (neoficiálne API, ktoré zvláda tokeny a požiadavky za nás)
- **Google Sheets:** Knižnica gspread (pre jednoduchú prácu s Google Sheets) a gspread-dataframe (pre zápis dát priamo z dátového rámca)
- **Spracovanie dát:** Knižnica pandas (štandard pre prácu s dátami v Pythone)
- **Automatizácia:** Cron job (pre pravidelné spúšťanie na Linux serveri)

## Krok 1: Príprava prostredia a knižníc

Na vašom privátnom serveri je potrebné mať nainštalovaný Python 3. Následne nainštalujte potrebné knižnice pomocou manažéra balíčkov pip:

```bash
pip install -r requirements.txt
```

## Krok 2: Overenie prístupu ku Google Sheets (Authentication)

Toto je najdôležitejší krok. Aby mohol váš skript bezpečne zapisovať do vášho Google Sheetu bez toho, aby ste v kóde ukladali svoje heslo, použijeme Google Service Account.

### Vytvorenie Service Account v Google Cloud:

1. Prejdite na [Google Cloud Console](https://console.cloud.google.com/).
2. Vytvorte nový projekt (napr. "Trends Scraper") alebo použite existujúci.
3. V menu prejdite na **APIs & Services > Library**.
4. Vyhľadajte a povoľte (Enable) dve kľúčové API: **Google Drive API** a **Google Sheets API**.
5. Prejdite do **APIs & Services > Credentials**.
6. Kliknite na **+ CREATE CREDENTIALS** a vyberte **Service Account**.
7. Pomenujte účet (napr. "sheets-writer"), kliknite **CREATE AND CONTINUE** a potom **DONE**.
8. V zozname credentials nájdite novovytvorený service account a kliknite naň.
9. Prejdite do záložky **KEYS**, kliknite na **ADD KEY > Create new key**.
10. Vyberte typ **JSON** a kliknite na **CREATE**. Tým sa vám stiahne \*.json súbor s kľúčami. Tento súbor je ako heslo, uchovajte ho v bezpečí na serveri a nikdy ho nedávajte do verejného repozitára (napr. GitHub)!

### **Váš Service Account Email:**

```
sheets-writer@invelity-49165.iam.gserviceaccount.com
```

### **Riešenie problému s kvótou:**

Keďže service account má plný Google Drive, vytvorte Google Sheet manuálne:

1. **Vytvorte nový Google Sheet:**

   - Choďte na [Google Sheets](https://sheets.google.com/)
   - Kliknite na **"+ Prázdny"** alebo **"Blank"**
   - Pomenujte ho **"Google Trends Monitoring"**

2. **Zdieľajte sheet s service accountom:**

   - Kliknite na **"Zdieľať"** (Share) vpravo hore
   - Vložte email: `sheets-writer@invelity-49165.iam.gserviceaccount.com`
   - Dajte mu práva **"Editor"**
   - Kliknite na **"Odoslať"**

3. **Otestujte pripojenie:**
   ```bash
   ./run_trends.sh
   ```
4. Uložte stiahnutý JSON súbor ako `service_account.json` v tomto adresári (`/var/www/Google-trends-data/`).

## Krok 3: Konfigurácia skriptu

Skript `trends_updater.py` je už vytvorený. Pred spustením upravte konfiguráciu v súbore podľa vašich potrieb:

- **KEYWORDS:** Zadajte kľúčové slová, ktoré chcete sledovať
- **GEO_MAPPING:** Mapovanie krajín na názvy tabov v Google Sheete
- **TIMEFRAME:** Časové obdobie (viac info: https://github.com/GeneralMills/pytrends)
- **SERVICE_ACCOUNT_FILE:** Cesta k JSON súboru so Service Account kľúčmi (už nastavená)
- **GOOGLE_SHEET_NAME:** Názov Google Sheet dokumentu

## Krok 4: Automatizácia na serveri (Cron job)

Aby sa skript spúšťal automaticky, napríklad každý pondelok o 3:00 ráno, nastavte na serveri cron job.

1. Otvorte editor cron tabuliek príkazom:

   ```bash
   crontab -e
   ```

2. Na koniec súboru pridajte nový riadok:
   ```bash
   # Spustiť skript na aktualizáciu Google Trends každý pondelok o 3:00
   0 3 * * 1 /usr/bin/python3 /var/www/Google-trends-data/trends_updater.py >> /var/www/Google-trends-data/trends_updater.log 2>&1
   ```

### Vysvetlenie príkazového riadku:

- `0 3 * * 1`: Znamená "v nultú minútu, tretiu hodinu, každý deň v mesiaci, každý mesiac, v prvý deň týždňa (pondelok)".
- `/usr/bin/python3`: Cesta k interpreteru Pythonu (môže sa líšiť, overte príkazom `which python3`).
- `/var/www/Google-trends-data/trends_updater.py`: Absolútna cesta k vášmu Python skriptu.
- `>> /var/www/Google-trends-data/trends_updater.log 2>&1`: Veľmi dôležité! Toto presmeruje všetok výstup (aj chybový) do log súboru. Ak niečo zlyhá, v tomto súbore nájdete príčinu.

## Spustenie skriptu manuálne

Pre testovanie môžete skript spustiť manuálne:

```bash
cd /var/www/Google-trends-data
python3 trends_updater.py
```

## 🚀 Deployment Guide

### Files to Commit to Git

**✅ Required files:**

- `trends_updater.py` - Main automation script
- `requirements.txt` - Python dependencies
- `run_trends.sh` - Convenience script
- `README.md` - This documentation
- `.gitignore` - Git ignore rules
- `DEPLOYMENT.md` - Detailed deployment guide

**🔧 Optional files:**

- `diagnose_connection.py` - Diagnostic script
- `get_service_account_email.py` - Helper script

**❌ Never commit:**

- `service_account.json` - Contains sensitive credentials
- `venv/` - Virtual environment (create on server)
- `*.log` - Log files
- `__pycache__/` - Python bytecode

### Quick Server Setup

1. **Clone repository:** `git clone <your-repo> Google-trends-data`
2. **Set up environment:** `python3 -m venv venv && source venv/bin/activate`
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Add service account:** Copy `service_account.json` to server (don't commit!)
5. **Create Google Sheet:** Name it "Google Trends Monitoring" and share with service account
6. **Test:** `./run_trends.sh`
7. **Automate:** Set up cron job (see Krok 4)

See `DEPLOYMENT.md` for detailed instructions.

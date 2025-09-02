# Google Trends Data Monitoring

Automatizovaný systém pre zbieranie a monitorovanie dát z Google Trends s ukladaním do Google Sheets.

## 🚀 Funkcie

- **Automatické zbieranie dát**: Trend data pre zadané kľúčové slová
- **Geografické filtre**: Podpora rôznych krajín (SK, CZ, Global)
- **Google Sheets integrácia**: Priamy export a formátovanie dát
- **Related Topics/Queries**: Zber súvisiacich tém a vyhľadávaní
- **Rate limiting**: Ochrana pred Google API limitmi
- **Cron automatizácia**: Pravidelné spúšťanie

## 📁 Štruktúra projektu

```
Google-trends-data/
├── main.py                 # Hlavný script
├── related_extractor.py    # Related Topics/Queries
├── config.py              # Konfigurácia
├── requirements.txt       # Dependencies
├── run.sh                 # Bash script
├── tests/                 # Utility scripts
│   ├── check_cron.sh      
│   ├── cron_examples.sh   
│   ├── diagnose_connection.py
│   ├── get_service_account_email.py
│   ├── run_trends.sh
│   └── setup_cron.sh
├── README.md              
├── PROJECT_SUMMARY.md     
└── DEPLOYMENT.md          
```

## ⚙️ Inštalácia

### 1. Klonovanie
```bash
git clone https://github.com/Martin-1182/google-trends.git
cd google-trends
```

### 2. Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Google API Setup
1. [Google Cloud Console](https://console.cloud.google.com/)
2. Vytvor Service Account
3. Stiahnuť JSON kľúč → `service_account.json`
4. Aktivovať Google Sheets API
5. Zdieľať Google Sheet so service account

### 4. Konfigurácia
Uprav `config.py`:
```python
KEYWORDS = ["online marketing", "seo"]
GEO_MAPPING = {'Slovensko': 'SK', 'Česko': 'CZ'}
SPREADSHEET_NAME = 'Google Trends Monitoring'
```

## 🏃‍♂️ Spustenie

### Základné dáta
```bash
python3 main.py
```

### Related Topics/Queries
```bash
python3 related_extractor.py
```

### Bash script
```bash
chmod +x run.sh
./run.sh
```

## 🤖 Automatizácia

### Cron setup
```bash
chmod +x tests/setup_cron.sh
./tests/setup_cron.sh
```

### Manuálne cron
```bash
crontab -e
# Každý deň o 9:00
0 9 * * * /var/www/Google-trends-data/tests/run_trends.sh >> /var/log/google_trends.log 2>&1
```

## 🔧 Riešenie problémov

### Rate Limiting (429)
- Zvýš `REQUEST_DELAY` v config.py na 60+ sekúnd
- Počkaj 1-2 hodiny

### Žiadne dáta
- Skús populárnejšie keywords
- Zmeň geo na `''` (global)
- Dlhší timeframe

### Related data chyby
- Známa chyba v pytrends library
- Funguje lepšie s globálnymi, populárnymi termínmi

### Diagnostika
```bash
python3 tests/diagnose_connection.py
tail -f /var/log/google_trends.log
```

## 📊 Output dáta

### Trend Data
- Keyword, Country, Date, Value, isPartial

### Related Topics/Queries  
- topic_title, value, Type, Keyword, Country

---

**⚠️ Poznámka**: Projekt používa neoficiálne Google Trends API ktoré môže mať obmedzenia.

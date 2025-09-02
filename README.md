# 🚀 Google Trends Data Collector

**Automatické sťahovanie Google Trends dát a zápis do Google Sheets**

## 📋 Prehľad

Tento projekt automaticky zbiera dáta z Google Trends pre zadané kľúčové slová a krajiny, a zapisuje ich do Google Sheets. Ideálny pre marketing analýzu, SEO research a sledovanie trendov.

## ✨ Funkcie

- 📊 **Interest Over Time** - sledovanie popularity v čase
- 🏷️ **Related Topics** - súvisiace témy
- 🔍 **Related Queries** - súvisiace vyhľadávania  
- 🌍 **Multi-region support** - podpora viacerých krajín
- ⚙️ **Dynamická konfigurácia** - jednoduché nastavenie
- 🔄 **Automatizácia** - cron job podpora
- 📈 **Google Sheets integrácia** - priamy zápis dát

## 🛠️ Inštalácia

### 1. Klónovanie repozitára
```bash
git clone <your-repo> Google-trends-data
cd Google-trends-data
```

### 2. Vytvorenie virtuálneho prostredia
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 3. Inštalácia závislostí
```bash
pip install -r requirements.txt
```

### 4. Google Service Account setup

#### A) Vytvorenie Service Account:
1. Choďte na [Google Cloud Console](https://console.cloud.google.com/)
2. Vytvorte nový projekt alebo použite existujúci
3. Povoľte **Google Drive API** a **Google Sheets API**
4. Vytvorte Service Account:
   - **APIs & Services > Credentials**
   - **+ CREATE CREDENTIALS > Service Account**
   - Stiahnite JSON kľúč

#### B) Nastavenie Google Sheet:
1. Vytvorte nový Google Sheet s názvom **"Google Trends Monitoring"**
2. Zdieľajte ho s email adresou z service account JSON
3. Dajte práva **"Editor"**

#### C) Konfigurácia:
```bash
# Umiestnite service_account.json do root priečinka
cp /path/to/your/service_account.json ./service_account.json
```
## ⚙️ Konfigurácia

Upravte `config.py` podľa vašich potrieb:

```python
# Keywords to track
KEYWORDS = [
    "online marketing",
    "skincare",
    "your keyword"
]

# Geographic regions mapping
GEO_MAPPING = {
    "Slovensko": "SK",
    "Česko": "CZ", 
    "Poľsko": "PL"
}

# Time frame
TIMEFRAME = "today 3-m"  # posledné 3 mesiace

# Request delay (avoid rate limiting)
REQUEST_DELAY = 30  # sekúnd

# Data collection settings
COLLECT_INTEREST_OVER_TIME = True
COLLECT_RELATED_TOPICS = True
COLLECT_RELATED_QUERIES = True
```

## 🚀 Použitie

### Základné spustenie:
```bash
./run.sh
```

### Test s minimálnou konfiguráciou:
```bash
python3 test_minimal.py
```

### Testovanie nastavení:
```bash
python3 tests/test_config.py
```

## 🕒 Automatizácia (Cron Job)

### Nastavenie cron job:
```bash
crontab -e
```

### Pridajte riadok pre spustenie každý pondelok o 3:00:
```bash
0 3 * * 1 /var/www/Google-trends-data/run.sh >> /var/www/Google-trends-data/trends.log 2>&1
```

### Alternatívne časové nastavenia:
```bash
# Každý deň o 6:00
0 6 * * * /var/www/Google-trends-data/run.sh

# Každý týždeň v nedeľu o 23:00  
0 23 * * 0 /var/www/Google-trends-data/run.sh

# Každý mesiac 1. dňa o 2:00
0 2 1 * * /var/www/Google-trends-data/run.sh
```

## 📁 Štruktúra projektu

```
Google-trends-data/
├── main.py                 # 🎯 Hlavný script s GoogleTrendsCollector
├── config.py               # ⚙️ Dynamické nastavenia
├── config_test.py          # 🧪 Testovacia konfigurácia
├── run.sh                  # 🚀 Spúšťač
├── test_minimal.py         # 🧪 Minimálny test
├── service_account.json    # 🔐 Google Service Account (nepriložené)
├── requirements.txt        # 📦 Python závislosti
├── README.md              # 📖 Dokumentácia
├── DEPLOYMENT.md          # 🚀 Deployment návod
└── tests/                 # 🧪 Testovacie súbory
    ├── test_config.py
    ├── diagnose_connection.py
    ├── get_service_account_email.py
    └── ... (staré verzie)
```

## � API Rate Limiting

Google Trends má strict rate limiting. Riešenia:

### Odporúčané nastavenia:
- **REQUEST_DELAY**: minimálne 30-45 sekúnd
- **Málo keywords**: začnite s 2-3 keywords
- **Málo krajín**: začnite s 1-2 krajinami

### Test konfigurácia:
```python
# config_test.py - použije sa automaticky pri test_minimal.py
KEYWORDS = ["skincare"]
GEO_MAPPING = {"Slovensko": "SK"}  
REQUEST_DELAY = 45
COLLECT_RELATED_TOPICS = False    # vypnuté pre testing
COLLECT_RELATED_QUERIES = False   # vypnuté pre testing
```

## 📊 Output dáta

Dáta sa zapisujú do Google Sheets s nasledovnou štruktúrou:

### Sheet: "Interest Over Time"
| Date | Keyword | Country | Interest |
|------|---------|---------|----------|
| 2024-01-01 | skincare | SK | 85 |

### Sheet: "Related Topics" 
| Keyword | Country | Topic | Value | Type |
|---------|---------|-------|-------|------|
| skincare | SK | korean skincare | 100 | rising |

### Sheet: "Related Queries"
| Keyword | Country | Query | Value | Type |
|---------|---------|-------|-------|------|
| skincare | SK | skincare routine | 85 | top |

## 🔍 Troubleshooting

### Chyba 429 (Rate Limiting):
```bash
# Zvýšte delay v config.py
REQUEST_DELAY = 45  # alebo viac

# Znížte počet keywords/krajín
KEYWORDS = ["skincare"]  # testujte s 1 keyword
```

### Chyba autentifikácie:
```bash
# Skontrolujte service account
python3 tests/diagnose_connection.py

# Overte email service account
python3 tests/get_service_account_email.py
```

### Prázdne dáta:
- Niektoré keywords nemajú dostatok dát
- Skúste populárnejšie keywords
- Zmente timeframe na dlhšie obdobie

## 📝 Loggovanie

Logy sa zapisují automaticky:
```bash
# Pozrite najnovšie logy
tail -f trends.log

# Celý log
cat trends.log
```

## 🤝 Podpora

Pre problémy alebo otázky:
1. Skontrolujte logy
2. Spustite diagnostické testy
3. Overte Google Sheets prístup

## 📄 Licencia

MIT License - použite a upravujte podľa potreby.

---
**⭐ Ak vám tento projekt pomohol, dajte mu star na GitHub!**

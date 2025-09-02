# Google Trends Data Monitoring - Project Summary

## 🎯 Účel
Automatizovaný systém pre zbieranie Google Trends dát s ukladaním do Google Sheets.

## 🏗️ Architektúra

### Core Components
- **main.py**: Hlavný data collector
- **related_extractor.py**: Related Topics/Queries extractor  
- **config.py**: Centrálna konfigurácia
- **Google Sheets API**: Export a formátovanie

### Kľúčové funkcie
1. Interest Over Time data collection
2. Multi-region support (SK, CZ, Global)
3. Related Topics/Queries extraction
4. Rate limiting protection
5. Cron automation support

## 🔧 Tech Stack
- **pytrends**: Google Trends API (unofficial)
- **gspread**: Google Sheets integration
- **pandas**: Data manipulation
- **cron**: Automation scheduling

## 📊 Data Structure

### Trend Data
```
Keyword | Country | Date | Value | isPartial
```

### Related Data
```
topic_title | value | Type | Keyword | Country | Date
```

## 🚨 Known Issues

### API Limitations
- **Rate Limiting**: Google 429 errors
- **Related Data**: PyTrends library bugs
- **Data Availability**: Limited for less popular terms

### Solutions
1. **429 Errors**: Increase delays to 60+ seconds
2. **Related Bugs**: Use popular, global keywords
3. **No Data**: Try broader geo settings

## ✅ Best Practices

### Stable Data Collection
- Use popular keywords
- Set REQUEST_DELAY to 60+ seconds  
- Schedule cron jobs at different times
- Monitor logs for rate limiting

### Production Setup
- Proper logging setup
- Retry mechanisms
- Service account backup
- Regular monitoring

## 📈 Future Enhancements
- Web dashboard
- Database storage
- Real-time alerts
- Enhanced error handling

---

**Status**: Production ready for basic trend collection. Related Topics/Queries in beta due to API limitations.

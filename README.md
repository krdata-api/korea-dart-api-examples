# KRDART — Korea DART API Examples

[![Live](https://img.shields.io/badge/Live-dart.ryanpp.com-2b7fff)](https://dart.ryanpp.com)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-6BA539)](https://dart.ryanpp.com/openapi.yaml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Runnable examples for **KRDART** ([dart.ryanpp.com](https://dart.ryanpp.com)) — English JSON on top of Korea's DART filings, plus Altman Z (EM) + Piotroski-style F (5 signals) distress signals for KOSPI/KOSDAQ listed companies.

## Try it in 30 seconds

1. Get a free key on [RapidAPI](https://rapidapi.com/krdartapi/api/krdart) (Basic plan, 3,000 requests/month).
   Also available on [api.market](https://api.market/store/krdart/krdart-financials).
2. Run:

**Python** (needs `requests`):
```bash
RAPIDAPI_KEY=your_key python examples/python/quickstart.py
```

**Node.js** (>= 18):
```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs
```

**Postman**:
Import `examples/dart-api.postman_collection.json` and set the `rapidapi_key` variable.

## Common recipes

All recipes use:
```python
BASE = "https://krdart.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": "your_key", "X-RapidAPI-Host": "krdart.p.rapidapi.com"}
```

### Screen KOSPI for going-concern doubt
```python
events = requests.get(f"{BASE}/events/recent", headers=HEADERS,
                      params={"days": 90, "type": "GOING_CONCERN", "limit": 500}).json()
watchlist = {ev["corp_code"] for ev in events["results"]}
```

### Distress heatmap for a portfolio
```python
portfolio = ["00126380", "00164779", "00164742"]  # Samsung, LG, SK Hynix
for code in portfolio:
    d = requests.get(f"{BASE}/distress/{code}", headers=HEADERS).json()
    print(f"{code:10s} Altman {d['altman_grade']:8s} F={d['piotroski_f']} Risk {d['composite_grade']}")
```

### Financial ratios in English
```javascript
const fin = await (await fetch("https://krdart.p.rapidapi.com/financials/00126380?year=2024", {
  headers: { "X-RapidAPI-Key": "your_key", "X-RapidAPI-Host": "krdart.p.rapidapi.com" },
})).json();
const map = Object.fromEntries(fin.items.map(x => [x.account_name_en, x.current_amount]));
console.log("Current ratio:", map.current_assets / map.current_liabilities);
console.log("ROA:",         map.net_income / map.total_assets);
```

## Endpoints reference

| Method | Path | Purpose |
|---|---|---|
| GET | `/companies/search?q=` | Search by Korean/English name or ticker |
| GET | `/companies/{corp_code}` | Master record |
| GET | `/financials/{corp_code}` | Statements with English labels |
| GET | `/distress/{corp_code}` | Altman Z + Piotroski F + composite risk |
| GET | `/events/recent` | Cross-market risk-event feed |
| GET | `/health` | Uptime + coverage count |

Full spec: [openapi.yaml](https://dart.ryanpp.com/openapi.yaml).

## Not investment advice

Underlying data comes from Korea's Financial Supervisory Service (FSS) DART system.
We publish derived indicators only. Each response references the DART `rcept_no` so
you can pull the original filing from [dart.fss.or.kr](https://dart.fss.or.kr).

"""
Korea DART Corporate API — Python quickstart.

Get a free key (Basic plan, 3,000 requests/month): https://rapidapi.com/krdartapi/api/krdart
Docs: https://dart.ryanpp.com/openapi.yaml

    RAPIDAPI_KEY=your_key python quickstart.py
"""

import os

import requests

BASE = "https://krdart.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": "krdart.p.rapidapi.com",
}


def search(query: str, limit: int = 10) -> list[dict]:
    r = requests.get(f"{BASE}/companies/search", params={"q": query, "limit": limit}, headers=HEADERS)
    r.raise_for_status()
    return r.json()["results"]


def company(corp_code: str) -> dict:
    r = requests.get(f"{BASE}/companies/{corp_code}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def financials(corp_code: str, year: int = 2024, reprt: str = "11011") -> dict:
    r = requests.get(f"{BASE}/financials/{corp_code}", params={"year": year, "reprt": reprt}, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def distress(corp_code: str) -> dict:
    r = requests.get(f"{BASE}/distress/{corp_code}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def events(days: int = 7, event_type: str | None = None, limit: int = 50) -> list[dict]:
    params = {"days": days, "limit": limit}
    if event_type:
        params["type"] = event_type
    r = requests.get(f"{BASE}/events/recent", params=params, headers=HEADERS)
    r.raise_for_status()
    return r.json()["results"]


if __name__ == "__main__":
    # 1) find Samsung Electronics
    hits = search("samsung", limit=3)
    print("SEARCH →", [(h["corp_code"], h["corp_name_eng"]) for h in hits])

    samsung = hits[0]
    code = samsung["corp_code"]

    # 2) master
    print("COMPANY →", company(code))

    # 3) 2024 financials (English labels)
    fin = financials(code, year=2024)
    print(f"FINANCIALS → {fin['count']} items across BS/IS")
    for item in fin["items"][:5]:
        print(f"  {item['statement']:20s} {item['account_name_en']:30s} {item['current_amount']:,}")

    # 4) distress signal
    print("DISTRESS →", distress(code))

    # 5) recent risk events across market
    delistings = events(days=30, event_type="DELISTING_RISK", limit=10)
    print(f"DELISTING_RISK (30d) → {len(delistings)} events")
    for ev in delistings[:5]:
        print(f"  {ev['event_dt']}  sev={ev['severity']}  {ev['corp_name']}  {ev['detail'][:80]}")

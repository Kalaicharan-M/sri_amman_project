import os
import time
import requests
from pathlib import Path
from flask import Flask, render_template
from dotenv import load_dotenv

# Load .env from project root (Render uses env vars directly)
load_dotenv(Path(__file__).parent / ".env")
app = Flask(__name__)

# Fallback prices when API fails or no key
DEFAULT_GOLD_22K = "6,750"
DEFAULT_SILVER = "88.00"

# Cache live rates for 1 hour (saves API quota, improves reliability)
_rates_cache = {"gold": None, "silver": None, "updated": 0, "timestamp": None}
CACHE_SECONDS = 3600  # 1 hour

def fetch_live_rates():
    """Fetch live gold (22k) and silver prices in INR/gram using MetalpriceAPI (free tier: 100 req/month)."""
    now = time.time()
    if _rates_cache["gold"] and (now - _rates_cache["updated"]) < CACHE_SECONDS:
        return _rates_cache["gold"], _rates_cache["silver"], _rates_cache.get("timestamp")

    api_key = os.environ.get("METALPRICEAPI_KEY")
    if not api_key:
        return None, None, None

    try:
        url = "https://api.metalpriceapi.com/v1/latest"
        params = {"api_key": api_key, "base": "USD", "currencies": "INR,XAU,XAG"}
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()

        if not data.get("success") or "rates" not in data:
            return None, None, None

        rates = data["rates"]
        inr_per_usd = rates.get("INR")
        usd_per_oz_gold = rates.get("USDXAU")
        usd_per_oz_silver = rates.get("USDXAG")

        if not all([inr_per_usd, usd_per_oz_gold, usd_per_oz_silver]):
            return None, None, None

        # 1 troy oz = 31.1035 grams; 22k = 22/24 of 24k gold
        grams_per_oz = 31.1035
        gold_22k_per_gram_inr = (usd_per_oz_gold / grams_per_oz) * (22 / 24) * inr_per_usd
        silver_per_gram_inr = (usd_per_oz_silver / grams_per_oz) * inr_per_usd

        gold_str = f"{gold_22k_per_gram_inr:,.0f}"
        silver_str = f"{silver_per_gram_inr:,.2f}"
        from datetime import datetime
        ts = datetime.now().strftime("%d %b, %I:%M %p")
        _rates_cache["gold"] = gold_str
        _rates_cache["silver"] = silver_str
        _rates_cache["updated"] = now
        _rates_cache["timestamp"] = ts
        return gold_str, silver_str, ts
    except Exception:
        # Use cached values if API fails and we have them
        if _rates_cache["gold"]:
            return _rates_cache["gold"], _rates_cache["silver"], _rates_cache.get("timestamp")
        return None, None, None

# In-memory database with Live Unsplash URLs for immediate rendering
NEW_ARRIVALS = [
    {
        "id": 1,
        "name": "Sri Amman Jewellery 1 - Indian Temple Jewellery",
        "price": "115,000",
        "image": "https://plus.unsplash.com/premium_photo-1681276170092-446cd1b5b32d?q=80&w=688&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    },
    {
        "id": 2,
        "name": "Sri Amman Jewellery 2 - Contemporary Gold",
        "price": "85,000",
        "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=400&auto=format&fit=crop"
    },
    {
        "id": 3,
        "name": "Sri Amman Jewellery 3 - Diamond Set",
        "price": "250,000",
        "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=400&auto=format&fit=crop"
    },
    {
        "id": 4,
        "name": "Sri Amman Jewellery 4 - Bridal Choker",
        "price": "195,000",
        "image": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?q=80&w=400&auto=format&fit=crop"
    }
]

@app.route('/')
def home():
    gold_price, silver_price, last_updated = fetch_live_rates()
    if gold_price is None:
        gold_price = DEFAULT_GOLD_22K
    if silver_price is None:
        silver_price = DEFAULT_SILVER
    return render_template('index.html', products=NEW_ARRIVALS, gold_price=gold_price, silver_price=silver_price, last_updated=last_updated)

if __name__ == '__main__':
    # host='0.0.0.0' = accessible on local network (Redmi as server)
    # debug=False for Redmi (saves CPU/RAM); use True for local dev
    # threaded=False reduces memory on low-resource devices
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
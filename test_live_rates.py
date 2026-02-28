#!/usr/bin/env python3
"""Test that live gold/silver rates work correctly."""
import sys
from pathlib import Path

# Ensure we're in project root
sys.path.insert(0, str(Path(__file__).parent))

def test_api_key():
    from dotenv import load_dotenv
    import os
    load_dotenv(Path(__file__).parent / ".env")
    key = os.environ.get("METALPRICEAPI_KEY")
    assert key and len(key) > 10, "METALPRICEAPI_KEY not loaded from .env"
    print("OK: API key loaded")

def test_fetch_rates():
    from app import fetch_live_rates, DEFAULT_GOLD_22K, DEFAULT_SILVER
    g, s, ts = fetch_live_rates()
    assert g and s, "fetch_live_rates returned empty"
    assert g != DEFAULT_GOLD_22K or s != DEFAULT_SILVER, "Using fallback - API may have failed"
    print(f"OK: Gold Rs.{g}/g, Silver Rs.{s}/g, Updated {ts}")

def test_flask_response():
    from app import app
    with app.test_client() as c:
        r = c.get("/")
        assert r.status_code == 200
        html = r.data.decode()
        assert "LIVE RATE (INR)" in html
        assert "GOLD 22k" in html
        assert "SILVER" in html
        assert "Updated" in html
    print("OK: Flask page renders correctly")

if __name__ == "__main__":
    try:
        test_api_key()
        test_fetch_rates()
        test_flask_response()
        print("\n--- All tests passed ---")
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)

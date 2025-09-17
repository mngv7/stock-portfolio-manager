import yfinance as yf
import json
import pandas as pd
from pymemcache.client.base import Client
from app.services.parameter_store.parameter_store import fetch_parameter_local

MEMCACHED_ENDPOINT = fetch_parameter_local("/n11592931/memcached/endpoint")
CACHE_TTL = 3600

memcached_client = Client(MEMCACHED_ENDPOINT)

def ticker_cached_fetch(ticker: str):
    try:
        value = memcached_client.get(ticker)
    except Exception as e:
        print(f"Memcached error: {e}")

    if value:
        return value.decode('utf-8')

    response = yf.Ticker(ticker)

    data = response.info
    fetched_value = json.dumps(data, allow_nan=False).encode("utf-8")

    memcached_client.set(ticker, fetched_value, expire=CACHE_TTL)

    return fetched_value


if __name__ == "__main__":
    ticker_cached_fetch("AAPL")

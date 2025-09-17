import yfinance as yf
import json
import pandas as pd
from pymemcache.client.base import Client
from app.services.parameter_store.parameter_store import fetch_parameter_local

MEMCACHED_ENDPOINT = fetch_parameter_local("/n11592931/memcached/endpoint")
CACHE_TTL = 3600

memcached_client = Client(MEMCACHED_ENDPOINT)

class CachedTicker:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self._ticker = yf.Ticker(symbol)
    
    @property
    def info(self):
        value = memcached_client.get(f"{self.symbol}:info")
        if value:
            return json.loads(value.decode("utf-8"))
        
        data = self._ticker.info
        memcached_client.set(f"{self.symbol}:info", json.dumps(data, allow_nan=False).encode("utf-8"), expire=CACHE_TTL)
        return data

    def history(self, *args, **kwargs):
        key = f"{self.symbol}:history:{args}:{kwargs}"
        value = memcached_client.get(key)
        if value:
            return pd.DataFrame(json.loads(value.decode("utf-8")))
        
        df = self._ticker.history(*args, **kwargs)
        memcached_client.set(key, df.to_json().encode("utf-8"), expire=CACHE_TTL)
        return df

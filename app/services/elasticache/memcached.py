import yfinance as yf
import json
import pandas as pd
from pymemcache.client.base import Client
from app.services.parameter_store.parameter_store import fetch_parameter_local
import re
import io

MEMCACHED_ENDPOINT = fetch_parameter_local("/n11592931/memcached/endpoint")
CACHE_TTL = 1800

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
        raw_key = f"{self.symbol}:history:{args}:{kwargs}"
        key = re.sub(r"\s+", "", raw_key)

        value = memcached_client.get(key)
        if value:
            df = pd.read_json(io.StringIO(value.decode("utf-8")), convert_dates=True)
            if isinstance(df.index, pd.DatetimeIndex) and df.index.tz is None:
                df.index = df.index.tz_localize('UTC')
            return df

        # Cache miss
        df = self._ticker.history(*args, **kwargs)
        memcached_client.set(
            key,
            df.to_json(date_format='iso').encode("utf-8"),
            expire=CACHE_TTL
        )
        return df

import time
import requests
from pymemcache.client.base import Client
from app.services.parameter_store.parameter_store import fetch_parameter_local

MEMCACHED_ENDPOINT = fetch_parameter_local("/n11592931/memcached/endpoint")
URL = "https://pymemcache.readthedocs.io/en/latest/getting_started.html"
CACHE_TTL = 60  # Cache time-to-live in seconds

# Global memcached client
memcached_client = Client(MEMCACHED_ENDPOINT)

def cached_fetch(url):
    print(f"Fetching {url}")
    value = memcached_client.get(url)
    if value:
        print("Cache hit")
        return value.decode('utf-8')
    
    print("Cache miss.  Fetching from URL")
    response = requests.get(url)
    # We need to encode the string, as pymemcache expects ASCII only
    fetched_value = response.text.encode()
    print(f"Fetched {len(fetched_value)} bytes")
    memcached_client.set(url, fetched_value, expire=CACHE_TTL)
    print("Stored in cache")
    return fetched_value

for i in range(10):
    start = time.time()
    print(f"Fetch {i}:")
    try:
        res = cached_fetch(URL)
        print(f"cached: {len(res)} bytes")
        cached_fetch(URL)
        print(f"Fetch {i} completed")
    except Exception as e:
        print("Error occurred")
        print(e)
    if i == 0:
        print(f"not cached: {time.time() - start:.2f}s")    
    else: 
        print(f"cached: {time.time() - start:.2f}s")
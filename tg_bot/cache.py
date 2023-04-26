from math import inf
from cachetools import TTLCache, LRUCache


migration_cache = TTLCache(maxsize=inf, ttl=10.0)
admin_cache = LRUCache(maxsize=inf)

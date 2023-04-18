from math import inf
from cachetools import TTLCache


cache = TTLCache(maxsize=inf, ttl=10.0)

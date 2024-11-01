#!/usr/bin/env python3
"""LIFO caching system"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO cache - removes last item added when full"""

    def __init__(self):
        """Initialize cache"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add item to cache with LIFO removal"""
        if key and item:
            if key in self.cache_data:
                self.order.remove(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                discard = self.order.pop()
                del self.cache_data[discard]
                print(f"DISCARD: {discard}")

            self.order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Get item from cache"""
        return self.cache_data.get(key) if key else None

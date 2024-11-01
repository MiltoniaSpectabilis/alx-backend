#!/usr/bin/env python3
"""LRU caching system"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU cache - removes least recently used item when full"""

    def __init__(self):
        """Initialize cache"""
        super().__init__()
        self.usage = []

    def put(self, key, item):
        """Add item to cache with LRU removal"""
        if key and item:
            if key in self.cache_data:
                self.usage.remove(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                discard = self.usage.pop(0)
                del self.cache_data[discard]
                print(f"DISCARD: {discard}")

            self.usage.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Get item from cache and update usage"""
        if key and key in self.cache_data:
            self.usage.remove(key)
            self.usage.append(key)
            return self.cache_data[key]
        return None

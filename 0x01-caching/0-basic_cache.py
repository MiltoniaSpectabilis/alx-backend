#!/usr/bin/env python3
"""Basic caching system"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic cache - no limit"""

    def put(self, key, item):
        """Add item to cache"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Get item from cache"""
        return self.cache_data.get(key) if key else None

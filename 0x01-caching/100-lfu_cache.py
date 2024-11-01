#!/usr/bin/env python3
"""LFU caching system"""
from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """LFU cache - removes least frequently used item when full"""

    def __init__(self):
        """Initialize cache"""
        super().__init__()
        self.usage = []
        self.frequency = defaultdict(int)

    def put(self, key, item):
        """Add item to cache with LFU removal"""
        if key and item:
            if key in self.cache_data:
                self.usage.remove(key)
                self.frequency[key] += 1
            elif len(self.cache_data) >= self.MAX_ITEMS:
                min_freq = min(self.frequency.values())
                lfu_keys = [k for k, v in self.frequency.items()
                            if v == min_freq]

                if len(lfu_keys) == 1:
                    discard = lfu_keys[0]
                else:
                    # If multiple items have same frequency, use LRU
                    for k in self.usage:
                        if k in lfu_keys:
                            discard = k
                            break

                self.usage.remove(discard)
                del self.cache_data[discard]
                del self.frequency[discard]
                print(f"DISCARD: {discard}")
            else:
                self.frequency[key] = 0

            self.usage.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Get item from cache and update frequency/usage"""
        if key and key in self.cache_data:
            self.usage.remove(key)
            self.usage.append(key)
            self.frequency[key] += 1
            return self.cache_data[key]
        return None

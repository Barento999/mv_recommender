"""
Performance Cache Manager

Caches recommendation results for faster inference.
Implements TTL (time-to-live) expiration and cache invalidation.
"""

import time
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
import threading

logger = logging.getLogger(__name__)


class PerformanceCache:
    """Cache recommendation results for performance optimization."""
    
    def __init__(self, ttl_seconds: int = 3600, max_entries: int = 10000):
        """
        Initialize cache.
        
        Args:
            ttl_seconds: Time-to-live for cache entries (default 1 hour)
            max_entries: Maximum number of entries before cleanup
        """
        self.cache: Dict[str, Dict] = {}
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self.lock = threading.Lock()  # Thread-safe cache
        
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_saves': 0,
        }
    
    def get_cache_key(self, user_id: str, model_name: str, limit: int = 10) -> str:
        """
        Generate cache key for a recommendation request.
        
        Args:
            user_id: User ID
            model_name: Model identifier
            limit: Limit parameter
            
        Returns:
            Cache key
        """
        return f"{model_name}:{user_id}:{limit}"
    
    def get(self, key: str) -> Optional[List[Tuple[str, float]]]:
        """
        Get cached recommendations.
        
        Args:
            key: Cache key
            
        Returns:
            Cached recommendations or None if expired/missing
        """
        with self.lock:
            if key not in self.cache:
                self.stats['misses'] += 1
                return None
            
            entry = self.cache[key]
            
            # Check expiration
            if time.time() > entry['expires_at']:
                logger.debug(f"[Cache] Entry expired: {key}")
                del self.cache[key]
                self.stats['misses'] += 1
                return None
            
            # Cache hit
            entry['last_accessed'] = time.time()
            entry['access_count'] += 1
            self.stats['hits'] += 1
            
            logger.debug(f"[Cache] Hit: {key} (accessed {entry['access_count']} times)")
            return entry['value']
    
    def set(self, key: str, recommendations: List[Tuple[str, float]], 
            metadata: Dict = None) -> None:
        """
        Cache recommendations.
        
        Args:
            key: Cache key
            recommendations: List of (movie_id, score) tuples
            metadata: Optional metadata (model version, etc.)
        """
        with self.lock:
            # Cleanup if needed
            if len(self.cache) >= self.max_entries:
                self._cleanup_lru()
            
            entry = {
                'value': recommendations,
                'created_at': time.time(),
                'expires_at': time.time() + self.ttl_seconds,
                'last_accessed': time.time(),
                'access_count': 0,
                'metadata': metadata or {}
            }
            
            self.cache[key] = entry
            self.stats['total_saves'] += 1
            
            logger.debug(f"[Cache] Stored: {key} ({len(recommendations)} items)")
    
    def invalidate(self, pattern: str = None, user_id: str = None, 
                   model_name: str = None) -> int:
        """
        Invalidate cache entries.
        
        Args:
            pattern: Pattern to match (e.g., "model_v1:*")
            user_id: Invalidate all entries for a user
            model_name: Invalidate all entries for a model
            
        Returns:
            Number of entries invalidated
        """
        with self.lock:
            initial_size = len(self.cache)
            
            if user_id:
                # Invalidate by user
                keys_to_delete = [k for k in self.cache.keys() if user_id in k]
            elif model_name:
                # Invalidate by model
                keys_to_delete = [k for k in self.cache.keys() if k.startswith(model_name)]
            elif pattern:
                # Invalidate by pattern
                keys_to_delete = [
                    k for k in self.cache.keys() 
                    if self._matches_pattern(k, pattern)
                ]
            else:
                # Clear all
                keys_to_delete = list(self.cache.keys())
            
            for key in keys_to_delete:
                del self.cache[key]
            
            invalidated = initial_size - len(self.cache)
            logger.info(f"[Cache] Invalidated {invalidated} entries")
            
            return invalidated
    
    def _cleanup_lru(self) -> None:
        """Remove least recently used entries."""
        # Sort by access count and last accessed time
        sorted_keys = sorted(
            self.cache.keys(),
            key=lambda k: (self.cache[k]['access_count'], self.cache[k]['last_accessed'])
        )
        
        # Remove bottom 20%
        to_remove = len(self.cache) // 5
        for key in sorted_keys[:to_remove]:
            del self.cache[key]
        
        self.stats['evictions'] += to_remove
        logger.info(f"[Cache] LRU cleanup: removed {to_remove} entries")
    
    def _matches_pattern(self, key: str, pattern: str) -> bool:
        """Check if key matches pattern (simple glob)."""
        # Simple pattern matching: * means any characters
        pattern = pattern.replace('*', '.*')
        import re
        return bool(re.match(pattern, key))
    
    def clear(self) -> None:
        """Clear entire cache."""
        with self.lock:
            self.cache.clear()
            logger.info("[Cache] Cache cleared")
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_entries,
                'ttl_seconds': self.ttl_seconds,
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'total_requests': total_requests,
                'hit_rate': float(hit_rate),
                'total_saves': self.stats['total_saves'],
                'evictions': self.stats['evictions'],
            }
    
    def get_memory_usage(self) -> Dict:
        """Estimate memory usage."""
        try:
            import sys
            
            total_bytes = 0
            for key, entry in self.cache.items():
                total_bytes += sys.getsizeof(key)
                total_bytes += sys.getsizeof(entry['value'])
            
            return {
                'estimated_bytes': total_bytes,
                'estimated_mb': total_bytes / (1024 * 1024),
                'entries': len(self.cache),
            }
        except Exception as e:
            logger.warning(f"[Cache] Could not estimate memory: {str(e)}")
            return {}
    
    def export_stats_report(self) -> str:
        """Generate cache statistics report."""
        stats = self.get_stats()
        memory = self.get_memory_usage()
        
        report = []
        report.append("="*50)
        report.append("CACHE STATISTICS REPORT")
        report.append("="*50)
        report.append(f"Cache Size: {stats['size']}/{stats['max_size']} entries")
        report.append(f"TTL: {stats['ttl_seconds']}s")
        report.append("")
        report.append("Performance:")
        report.append(f"  Hits: {stats['hits']}")
        report.append(f"  Misses: {stats['misses']}")
        report.append(f"  Total Requests: {stats['total_requests']}")
        report.append(f"  Hit Rate: {stats['hit_rate']:.1f}%")
        report.append(f"  Total Saves: {stats['total_saves']}")
        report.append(f"  Evictions: {stats['evictions']}")
        report.append("")
        
        if memory:
            report.append("Memory Usage:")
            report.append(f"  Estimated: {memory['estimated_mb']:.2f} MB")
            report.append(f"  Per Entry: {memory['estimated_bytes'] / memory['entries']:.0f} bytes" 
                         if memory['entries'] > 0 else "  Per Entry: N/A")
        
        report.append("="*50)
        
        return "\n".join(report)


# Global cache instance
_global_cache: Optional[PerformanceCache] = None


def get_global_cache() -> PerformanceCache:
    """Get or create global cache instance."""
    global _global_cache
    if _global_cache is None:
        _global_cache = PerformanceCache()
    return _global_cache


def set_global_cache(cache: PerformanceCache) -> None:
    """Set global cache instance."""
    global _global_cache
    _global_cache = cache

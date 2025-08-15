"""
Cache Manager Utility
Professional caching and performance optimization for the dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timedelta
import hashlib
import json
import pickle

class CacheManager:
    """Professional caching system for dashboard performance optimization"""
    
    def __init__(self):
        """Initialize the cache manager"""
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0
        }
    
    def generate_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """
        Generate unique cache key for function and arguments
        
        Args:
            func_name: Name of the function
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            str: Unique cache key
        """
        # Create a hash of the function name and arguments
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': kwargs
        }
        
        # Convert to JSON string and hash it
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def cache_data(self, ttl_hours: int = 24):
        """
        Decorator for caching data with time-to-live
        
        Args:
            ttl_hours: Time to live in hours
            
        Returns:
            Decorated function
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self.generate_cache_key(func.__name__, *args, **kwargs)
                
                # Check if data exists in cache and is not expired
                cached_data = self._get_cached_data(cache_key)
                if cached_data is not None:
                    self.cache_stats['hits'] += 1
                    self.cache_stats['total_requests'] += 1
                    return cached_data['data']
                
                # Cache miss - execute function and cache result
                self.cache_stats['misses'] += 1
                self.cache_stats['total_requests'] += 1
                
                try:
                    result = func(*args, **kwargs)
                    self._cache_data(cache_key, result, ttl_hours)
                    return result
                except Exception as e:
                    st.error(f"Function execution failed: {str(e)}")
                    return None
            
            return wrapper
        return decorator
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached data if it exists and is not expired
        
        Args:
            cache_key: Cache key to retrieve
            
        Returns:
            Cached data dict or None if not found/expired
        """
        try:
            if cache_key in st.session_state:
                cached_data = st.session_state[cache_key]
                
                # Check if cache has expired
                if datetime.now() < cached_data['expires_at']:
                    return cached_data
                else:
                    # Remove expired cache
                    del st.session_state[cache_key]
            
            return None
        except Exception:
            return None
    
    def _cache_data(self, cache_key: str, data: Any, ttl_hours: int):
        """
        Cache data with expiration time
        
        Args:
            cache_key: Cache key
            data: Data to cache
            ttl_hours: Time to live in hours
        """
        try:
            cache_entry = {
                'data': data,
                'cached_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(hours=ttl_hours)
            }
            
            st.session_state[cache_key] = cache_entry
        except Exception as e:
            st.warning(f"Failed to cache data: {str(e)}")
    
    def clear_cache(self, pattern: Optional[str] = None):
        """
        Clear cache entries
        
        Args:
            pattern: Optional pattern to match cache keys
        """
        try:
            if pattern:
                # Clear cache keys matching pattern
                keys_to_remove = [
                    key for key in st.session_state.keys() 
                    if pattern in key and key.startswith('cache_')
                ]
                for key in keys_to_remove:
                    del st.session_state[key]
            else:
                # Clear all cache keys
                keys_to_remove = [
                    key for key in st.session_state.keys() 
                    if key.startswith('cache_')
                ]
                for key in keys_to_remove:
                    del st.session_state[key]
            
            st.success(f"Cache cleared successfully")
        except Exception as e:
            st.error(f"Failed to clear cache: {str(e)}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_stats['total_requests']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'cache_hits': self.cache_stats['hits'],
            'cache_misses': self.cache_stats['misses'],
            'hit_rate': round(hit_rate, 2),
            'cache_size': len([k for k in st.session_state.keys() if k.startswith('cache_')])
        }
    
    def display_cache_stats(self):
        """Display cache performance statistics"""
        stats = self.get_cache_stats()
        
        st.markdown("### Cache Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Requests", stats['total_requests'])
        
        with col2:
            st.metric("Cache Hits", stats['cache_hits'])
        
        with col3:
            st.metric("Cache Misses", stats['cache_misses'])
        
        with col4:
            st.metric("Hit Rate", f"{stats['hit_rate']}%")
        
        # Cache management controls
        st.markdown("### Cache Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear All Cache"):
                self.clear_cache()
        
        with col2:
            if st.button("Refresh Stats"):
                st.rerun()
    
    def optimize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame for better performance
        
        Args:
            df: DataFrame to optimize
            
        Returns:
            Optimized DataFrame
        """
        try:
            # Create a copy to avoid modifying original
            optimized_df = df.copy()
            
            # Optimize data types
            for col in optimized_df.columns:
                col_type = optimized_df[col].dtype
                
                # Optimize numeric columns
                if col_type in ['int64', 'float64']:
                    if col_type == 'int64':
                        # Downcast integers
                        optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='integer')
                    else:
                        # Downcast floats
                        optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='float')
                
                # Optimize object columns
                elif col_type == 'object':
                    # Check if column can be converted to category
                    if optimized_df[col].nunique() / len(optimized_df) < 0.5:
                        optimized_df[col] = optimized_df[col].astype('category')
            
            return optimized_df
            
        except Exception as e:
            st.warning(f"DataFrame optimization failed: {str(e)}")
            return df
    
    def cache_expensive_operation(self, operation_name: str, operation_func: Callable, 
                                *args, ttl_hours: int = 24, **kwargs) -> Any:
        """
        Cache expensive operations with automatic key generation
        
        Args:
            operation_name: Name of the operation
            operation_func: Function to execute
            *args: Function arguments
            ttl_hours: Cache TTL in hours
            **kwargs: Function keyword arguments
            
        Returns:
            Operation result
        """
        cache_key = f"cache_{operation_name}_{self.generate_cache_key(operation_func.__name__, *args, **kwargs)}"
        
        # Check cache first
        cached_result = self._get_cached_data(cache_key)
        if cached_result is not None:
            self.cache_stats['hits'] += 1
            self.cache_stats['total_requests'] += 1
            return cached_result['data']
        
        # Execute operation and cache result
        self.cache_stats['misses'] += 1
        self.cache_stats['total_requests'] += 1
        
        try:
            result = operation_func(*args, **kwargs)
            self._cache_data(cache_key, result, ttl_hours)
            return result
        except Exception as e:
            st.error(f"Operation failed: {str(e)}")
            return None 
"""
Cache utilities for WZML-X bot.
Provides TTLCache-based caching for user data and other frequently accessed data.
"""

from cachetools import TTLCache

# User data cache with 5-minute TTL, max 1000 entries
# Reduces database queries for frequently accessed user settings
user_settings_cache = TTLCache(maxsize=1000, ttl=300)


def get_cached_user_data(user_id: int, user_data: dict) -> dict:
    """
    Get user data with caching.
    
    Args:
        user_id: Telegram user ID
        user_data: Global user_data dict from bot module
        
    Returns:
        User settings dict (from cache if available)
    """
    if user_id in user_settings_cache:
        return user_settings_cache[user_id]
    
    result = user_data.get(user_id, {})
    user_settings_cache[user_id] = result
    return result


def invalidate_user_cache(user_id: int) -> None:
    """
    Invalidate cache for a specific user.
    
    Args:
        user_id: Telegram user ID to invalidate
    """
    user_settings_cache.pop(user_id, None)


def update_user_cache(user_id: int, data: dict) -> None:
    """
    Update cache for a specific user.
    
    Args:
        user_id: Telegram user ID
        data: New user data to cache
    """
    user_settings_cache[user_id] = data


def clear_user_cache() -> None:
    """Clear all cached user data."""
    user_settings_cache.clear()


# Download/upload session cache for reusing connections
session_cache = TTLCache(maxsize=100, ttl=600)  # 10-minute TTL


def get_cached_session(key: str):
    """Get cached session by key."""
    return session_cache.get(key)


def cache_session(key: str, session) -> None:
    """Cache a session."""
    session_cache[key] = session

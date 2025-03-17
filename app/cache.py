from datetime import datetime, timedelta, UTC
from typing import Dict, Any, Optional


class SimpleCache:
    """
    Simple in-memory cache.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    async def set(self, key: str, value: Any, expiry_seconds: int) -> None:
        """
        Sets a key-value pair in the cache with an expiry time.

        Args:
            key (str): The key to store in the cache.
            value (Any): The value to store.
            expiry_seconds (int): The number of seconds after which the cache entry expires.
        """
        expiry = datetime.now(UTC) + timedelta(seconds=expiry_seconds)
        self._cache[key] = {
            "value": value,
            "expiry": expiry
        }

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieves the value for the given key from the cache, if not expired.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[Any]: The cached value if it exists and is not expired; otherwise, None.
        """
        if key not in self._cache:
            return None

        cached_item = self._cache[key]
        if cached_item["expiry"] < datetime.now(UTC):
            del self._cache[key]
            return None

        return cached_item["value"]

    async def delete(self, key: str) -> bool:
        """
        Deletes a key-value pair from the cache.

        Args:
            key (str): The key to delete.

        Returns:
            bool: True if the key was deleted, False if the key was not found.
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    async def delete_pattern(self, pattern: str) -> int:
        """
        Deletes all key-value pairs whose keys match the given pattern.

        Args:
            pattern (str): A string pattern to match within the keys.

        Returns:
            int: The number of keys deleted.
        """
        keys_to_delete = [k for k in self._cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self._cache[key]
        return len(keys_to_delete)


cache = SimpleCache()

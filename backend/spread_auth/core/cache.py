from functools import lru_cache


class BaseCache:
    _cache = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def get(self, key):
        return self._cache.get(key, {})

    def set(self, key, value):
        self._cache[key] = value


class PermissionUsersCache(BaseCache):
    ...
    #
    # def load(self, data):
    #     self._cache = {item.topic_path: (item.hash, item.id,) for item in data}
    #
    # def update(self, data):
    #     self._cache = {**self._cache, **{item.topic_path: (item.hash, item.id,) for item in data}}

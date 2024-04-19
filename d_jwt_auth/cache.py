from typing import Any

from django.core.cache import cache


def get_cache(key: Any) -> Any:
    value = cache.get(key=key)
    cache.close()
    return value


def set_cache(key: Any, value: Any, timeout: int) -> None:
    cache.set(key=key, value=value, timeout=timeout)
    cache.close()


def delete_cache(key) -> bool:
    cache_delete = cache.delete(key=key)
    cache.close()
    return cache_delete


def clear_all_cache() -> None:
    cache.clear()


def incr_cache(key: Any) -> bool:
    incr = cache.incr(key=key)
    cache.close()
    return incr

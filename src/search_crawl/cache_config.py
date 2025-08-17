from functools import wraps
from typing import Any, Awaitable, Callable

import redis
from pydantic import BaseModel

r = redis.Redis.from_url("redis://@redis:6379", decode_responses=True)


class CacheConfig(BaseModel):
    readable: bool = True
    writable: bool = True
    ttl: int | None = 60 * 60 * 24

    def wrap_with_cache[R: Any, **P](
        self, cache_key: str, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if self.readable and (cached_value := r.json().get(cache_key)):
                return cached_value
            else:
                result = await func(*args, **kwargs)
                if self.writable:
                    r.json().set(cache_key, "$", result)
                    if self.ttl:
                        r.expire(cache_key, self.ttl)

                return result

        return wrapper

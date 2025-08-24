import os
from functools import wraps
from typing import Any, Awaitable, Callable, cast

import redis
from pydantic import BaseModel

r: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global r
    if r is None:
        r = redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
    return r


class CacheConfig(BaseModel):
    readable: bool = True
    writable: bool = True
    ttl: int | None = 60 * 60 * 24

    def wrap_with_cache[R: Any, **P](
        self, cache_key: str, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            r = get_redis()
            if self.readable and (cached_value := r.json().get(cache_key)):
                return cast(R, cached_value)
            else:
                result = await func(*args, **kwargs)
                if self.writable:
                    r.json().set(cache_key, "$", result)
                    if self.ttl:
                        r.expire(cache_key, self.ttl)

                return result

        return wrapper

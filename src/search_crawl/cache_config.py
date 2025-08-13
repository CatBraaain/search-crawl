from functools import wraps
from typing import Awaitable, Callable

from cashews import Command, cache
from cashews.ttl import TTL
from pydantic import BaseModel

cache.setup("disk://?directory=.cache&shards=0")


class CacheConfig(BaseModel):
    readable: bool = True
    writable: bool = True
    ttl: TTL = "24h"

    @property
    def disables(self) -> list[Command]:
        return [
            cmd
            for cmd, enabled in [
                (Command.GET, self.readable),
                (Command.SET, self.writable),
            ]
            if not enabled
        ]

    def wrap_with_cache[R, **P](
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        cached_func = cache(ttl=self.ttl)(func)

        @wraps(func)
        async def cached_func_with_disables(*args: P.args, **kwargs: P.kwargs) -> R:
            with cache.disabling(*self.disables):
                return await cached_func(*args, **kwargs)

        return cached_func_with_disables

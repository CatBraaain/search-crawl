from cashews import cache
from cashews.ttl import TTL
from pydantic import BaseModel

cache.setup("disk://?directory=.cache&shards=0")


class CacheConfig(BaseModel):
    readable: bool = True
    writable: bool = True
    ttl: TTL = "24h"

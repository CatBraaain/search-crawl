from collections.abc import AsyncGenerator

import pytest

from search_crawl_client import (
    ApiClient,
    CacheConfig,
    Configuration,
    DefaultApi,
)


@pytest.fixture
async def api() -> AsyncGenerator[DefaultApi]:
    config = Configuration(host="http://localhost:8000")
    async with ApiClient(config) as client:
        yield DefaultApi(client)


@pytest.fixture(
    params=[
        CacheConfig(readable=False, writable=True),
        CacheConfig(readable=True, writable=True),
    ],
    ids=["[without cache]", "[with cache]"],
)
def cache_config(request: pytest.FixtureRequest):
    return request.param

from collections.abc import AsyncGenerator

import pytest

from search_crawl_client import ApiClient, Configuration, DefaultApi


@pytest.fixture
async def api() -> AsyncGenerator[DefaultApi]:
    config = Configuration(host="http://localhost:8000")
    async with ApiClient(config) as client:
        yield DefaultApi(client)

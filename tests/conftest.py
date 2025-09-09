import os
from collections.abc import AsyncGenerator
from enum import StrEnum

import dotenv
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


@pytest.fixture
async def api_key() -> str:
    api_key = dotenv.get_key(".env", "GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    return api_key


@pytest.fixture(
    params=[
        CacheConfig(readable=False, writable=True),
        CacheConfig(readable=True, writable=True),
    ],
    ids=["[without cache]", "[with cache]"],
)
def cache_config(request: pytest.FixtureRequest):
    return request.param


class TestSite(StrEnum):
    EXAMPLE = "https://example.com/"
    QUOTES = "https://quotes.toscrape.com/"
    COUNTRY = "https://www.scrapethissite.com/pages/simple/"
    PRODUCTS = "https://web-scraping.dev/products"
    HOCKEY = "https://www.scrapethissite.com/pages/forms/?per_page=100"

import pytest

from search_crawl_client import (
    CacheConfig,
    CrawlRequest,
    DefaultApi,
)


@pytest.mark.parametrize(
    "url, page_length",
    [
        ("https://example.com", 1),
        ("https://web-scraping.dev/products", 5),
        ("https://www.scrapethissite.com/pages/forms/?per_page=100", 6),
        ("https://quotes.toscrape.com/", 10),
    ],
)
async def test_crawl_pagination(api: DefaultApi, url, page_length):
    res = await api.crawl(
        CrawlRequest(
            url=url,
            cache_config=CacheConfig(readable=True, writable=True),
        )
    )
    assert len(res) == page_length

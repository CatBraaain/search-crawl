from search_crawl_client import (
    CacheConfig,
    CrawlManyRequest,
    CrawlRequest,
    DefaultApi,
)


async def test_crawl(api: DefaultApi):
    res = await api.crawl(
        CrawlRequest(
            url="https://example.com",
            cache_config=CacheConfig(readable=False, writable=False),
        )
    )
    assert res


async def test_crawl_many(api: DefaultApi):
    res = await api.crawl_many(
        CrawlManyRequest(
            urls=[
                "https://example.com",
                "https://web-scraping.dev/products",
            ],
            cache_config=CacheConfig(readable=False, writable=False),
        )
    )
    assert len(res) == 2
    assert len(res[0]) == 1
    assert len(res[1]) == 5

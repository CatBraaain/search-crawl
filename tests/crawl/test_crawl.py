from search_crawl_client import (
    CacheConfig,
    CrawlManyRequest,
    CrawlRequest,
    DefaultApi,
)


async def test_crawl(api: DefaultApi, cache_config: CacheConfig):
    res = await api.crawl(
        CrawlRequest(
            url="https://example.com",
            cache_config=cache_config,
        )
    )
    assert res


async def test_crawl_many(api: DefaultApi, cache_config: CacheConfig):
    res = await api.crawl_many(
        CrawlManyRequest(
            urls=[
                "https://example.com",
                "https://web-scraping.dev/products",
            ],
            cache_config=cache_config,
        )
    )
    assert len(res) == 2
    assert len(res[0]) == 1
    assert len(res[1]) == 5

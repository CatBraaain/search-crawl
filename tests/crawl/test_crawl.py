from search_crawl_client import (
    CacheStrategy,
    CrawlManyRequest,
    CrawlRequest,
)


def test_crawl(api):
    res = api.crawl(
        CrawlRequest(
            url="https://example.com",
            cache_strategy=CacheStrategy(readable=False, writable=False),
        )
    )
    assert res


def test_crawl_many(api):
    res = api.crawl_many(
        CrawlManyRequest(
            urls=[
                "https://example.com",
                "https://web-scraping.dev/products",
            ],
            cache_strategy=CacheStrategy(readable=False, writable=False),
        )
    )
    assert len(res) == 2
    assert len(res[0]) == 1
    assert len(res[1]) == 5

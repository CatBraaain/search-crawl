from search_crawl_client.models import (
    CacheStrategy,
    CrawlApiArg,
    CrawlManyApiArg,
)


def test_crawl(api):
    res = api.crawl(
        CrawlApiArg(
            url="https://example.com",
            cache_strategy=CacheStrategy(readable=False, writable=False),
        )
    )
    assert res


def test_crawl_many(api):
    res = api.crawl_many(
        CrawlManyApiArg(
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

from search_crawl_client import ApiClient, Configuration
from search_crawl_client.api.default_api import DefaultApi
from search_crawl_client.models import (
    CacheStrategy,
    CrawlApiArg,
    CrawlManyApiArg,
)

config = Configuration(host="http://localhost:8000")
with ApiClient(config) as client:
    api = DefaultApi(client)


def test_healthz():
    res = api.healthz()
    assert res == "OK"


def test_search_general():
    res = api.search_general(q="ping")
    assert isinstance(res, list) and len(res) > 0


def test_search_images():
    res = api.search_images(q="ping")
    assert isinstance(res, list) and len(res) > 0


def test_crawl():
    res = api.crawl(
        CrawlApiArg(
            url="https://example.com",
            cache_strategy=CacheStrategy(readable=False, writable=False),
        )
    )
    assert res


def test_crawl_many():
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


def test_crawl_pagination():
    res = api.crawl(
        CrawlApiArg(
            url="https://web-scraping.dev/products",
            cache_strategy=CacheStrategy(readable=False, writable=False),
        )
    )
    print([r.url for r in res])
    assert len(res) == 5

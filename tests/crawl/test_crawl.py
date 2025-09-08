import pytest

from search_crawl_client import (
    CacheConfig,
    CrawlRequest,
    CrawlRequestWithUrl,
    CrawlRequestWithUrls,
    DefaultApi,
    SearchCrawlRequest,
    SearchRequest,
)


async def test_crawl(api: DefaultApi, cache_config: CacheConfig):
    res = await api.crawl(
        CrawlRequestWithUrl(
            url="https://example.com",
            cache_config=cache_config,
        )
    )
    assert res


async def test_crawl_many(api: DefaultApi, cache_config: CacheConfig):
    res = await api.crawl_many(
        CrawlRequestWithUrls(
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


@pytest.fixture(params=[1, 3], ids=lambda x: f"[max search results={x}]")
def max_results(request: pytest.FixtureRequest):
    return request.param


async def test_search_crawl(
    api: DefaultApi,
    max_results: int | None,
    cache_config: CacheConfig,
):
    res = await api.search_crawl(
        SearchCrawlRequest(
            search=SearchRequest(
                q="scraping test site",
                max_results=max_results,
            ),
            crawl=CrawlRequest(
                cache_config=cache_config,
            ),
        )
    )
    assert isinstance(res, list)
    if max_results is None:
        assert len(res) > 0
    else:
        assert len(res) == max_results

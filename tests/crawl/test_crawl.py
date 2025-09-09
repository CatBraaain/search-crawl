import pytest

from search_crawl_client import (
    CacheConfig,
    CrawlConfig,
    CrawlRequest,
    CrawlRequestWithUrl,
    CrawlRequestWithUrls,
    CrawlScope,
    DefaultApi,
    SearchCrawlRequest,
    SearchRequest,
)
from tests.conftest import TestSite


async def test_crawl(api: DefaultApi, cache_config: CacheConfig):
    res = await api.crawl(
        CrawlRequestWithUrl(
            url=TestSite.EXAMPLE,
            cache_config=cache_config,
        )
    )
    assert res


async def test_crawl_many(api: DefaultApi, cache_config: CacheConfig):
    crawl_results = await api.crawl_many(
        CrawlRequestWithUrls(
            urls=[
                TestSite.EXAMPLE,
                TestSite.PRODUCTS,
            ],
            crawl_config=CrawlConfig(crawl_scope=CrawlScope.PAGINATION),
            cache_config=cache_config,
        )
    )
    example_result, products_result = crawl_results

    assert len(crawl_results) == 2
    assert len(example_result) == 1
    assert len(products_result) == 5


@pytest.mark.parametrize(
    "max_results",
    [1, 3],
    ids=lambda x: f"[max_results={x}]",
)
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
    assert len(res) == max_results

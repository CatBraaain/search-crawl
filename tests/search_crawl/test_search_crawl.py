import pytest

from search_crawl_client import (
    BaseCrawlRequest,
    CacheConfig,
    DefaultApi,
    SearchCrawlRequest,
    SearchRequest,
)


@pytest.fixture(params=[1, 3])
def max_results(request: pytest.FixtureRequest):
    return request.param


async def test_crawl_search(api: DefaultApi, max_results: int | None):
    res = await api.crawl_search(
        SearchCrawlRequest(
            search=SearchRequest(
                q="scraping test site",
                max_results=max_results,
            ),
            crawl=BaseCrawlRequest(
                cache_config=CacheConfig(readable=True, writable=True),
            ),
        )
    )
    assert isinstance(res, list)
    if max_results is None:
        assert len(res) > 0
    else:
        assert len(res) == max_results

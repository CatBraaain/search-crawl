import pytest

from search_crawl_client import (
    BaseCrawlRequest,
    CacheConfig,
    DefaultApi,
    GeneralSearchCrawlRequest,
    GeneralSearchRequest,
    ImageSearchCrawlRequest,
    ImageSearchRequest,
)


@pytest.fixture(params=[1, 3])
def max_results(request: pytest.FixtureRequest):
    return request.param


async def test_crawl_search_general(api: DefaultApi, max_results: int | None):
    res = await api.crawl_search_general(
        GeneralSearchCrawlRequest(
            search=GeneralSearchRequest(
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


async def test_crawl_search_image(api: DefaultApi, max_results: int | None):
    res = await api.crawl_search_image(
        ImageSearchCrawlRequest(
            search=ImageSearchRequest(
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

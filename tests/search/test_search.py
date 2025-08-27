import pytest

from search_crawl_client import (
    CacheConfig,
    DefaultApi,
    GeneralSearchRequest,
    ImageSearchRequest,
)


@pytest.fixture(params=[None, 1, 3])
def max_results(request: pytest.FixtureRequest):
    return request.param


async def test_search_general(api: DefaultApi, max_results: int | None):
    res = await api.search_general(
        GeneralSearchRequest(
            q="ping",
            max_results=max_results,
            cache_config=CacheConfig(readable=False, writable=False),
        )
    )
    assert isinstance(res, list)
    if max_results is None:
        assert len(res) > 0
    else:
        assert len(res) == max_results


async def test_search_images(api: DefaultApi, max_results: int | None):
    res = await api.search_images(
        ImageSearchRequest(
            q="ping",
            max_results=max_results,
            cache_config=CacheConfig(readable=False, writable=False),
        )
    )
    assert isinstance(res, list)
    if max_results is None:
        assert len(res) > 0
    else:
        assert len(res) == max_results

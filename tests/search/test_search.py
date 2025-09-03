import pytest

from search_crawl_client import (
    CacheConfig,
    DefaultApi,
    SearchRequest,
)


@pytest.fixture(params=[None, 1, 3])
def max_results(request: pytest.FixtureRequest):
    return request.param


async def test_search(api: DefaultApi, max_results: int | None):
    res = await api.search(
        SearchRequest(
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

import pytest

from search_crawl_client import (
    CacheConfig,
    DefaultApi,
    SearchRequest,
)


@pytest.fixture(params=[None, 1, 3], ids=lambda x: f"[max search results={x}]")
def max_results(request: pytest.FixtureRequest) -> int | None:
    return request.param


async def test_search(
    api: DefaultApi,
    max_results: int | None,
    cache_config: CacheConfig,
):
    res = await api.search(
        SearchRequest(
            q="ping",
            max_results=max_results,
            cache_config=cache_config,
        )
    )
    assert isinstance(res, list)
    if max_results is None:
        assert len(res) > 0
    else:
        assert len(res) == max_results

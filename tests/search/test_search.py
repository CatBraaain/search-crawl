from search_crawl_client import (
    CacheConfig,
    DefaultApi,
    GeneralSearchRequest,
    ImageSearchRequest,
)


async def test_search_general(api: DefaultApi):
    res = await api.search_general(
        GeneralSearchRequest(
            q="ping",
            cache_config=CacheConfig(readable=False, writable=False),
        )
    )
    assert isinstance(res, list) and len(res) > 0


async def test_search_images(api: DefaultApi):
    res = await api.search_images(
        ImageSearchRequest(
            q="ping",
            cache_config=CacheConfig(readable=False, writable=False),
        )
    )
    assert isinstance(res, list) and len(res) > 0

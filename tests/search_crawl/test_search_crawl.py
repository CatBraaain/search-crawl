from search_crawl_client import (
    BaseCrawlRequest,
    CacheConfig,
    DefaultApi,
    GeneralSearchCrawlRequest,
    GeneralSearchRequest,
    ImageSearchCrawlRequest,
    ImageSearchRequest,
)


async def test_crawl_search_general(api: DefaultApi):
    res = await api.crawl_search_general(
        GeneralSearchCrawlRequest(
            search=GeneralSearchRequest(q="scraping test site"),
            crawl=BaseCrawlRequest(
                cache_config=CacheConfig(readable=True, writable=True),
            ),
        )
    )
    assert isinstance(res, list) and len(res) > 0


async def test_crawl_search_image(api: DefaultApi):
    res = await api.crawl_search_image(
        ImageSearchCrawlRequest(
            search=ImageSearchRequest(q="scraping test site"),
            crawl=BaseCrawlRequest(
                cache_config=CacheConfig(readable=True, writable=True),
            ),
        )
    )
    assert isinstance(res, list) and len(res) > 0

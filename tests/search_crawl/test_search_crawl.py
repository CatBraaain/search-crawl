from search_crawl_client import (
    BaseCrawlRequest,
    CacheStrategy,
    GeneralSearchCrawlRequest,
    GeneralSearchRequest,
    ImageSearchCrawlRequest,
    ImageSearchRequest,
)


def test_crawl_search_general(api):
    res = api.crawl_search_general(
        GeneralSearchCrawlRequest(
            search=GeneralSearchRequest(q="scraping test site"),
            crawl=BaseCrawlRequest(
                cache_strategy=CacheStrategy(readable=True, writable=True),
            ),
        )
    )
    assert isinstance(res, list) and len(res) > 0


def test_crawl_search_image(api):
    res = api.crawl_search_image(
        ImageSearchCrawlRequest(
            search=ImageSearchRequest(q="scraping test site"),
            crawl=BaseCrawlRequest(
                cache_strategy=CacheStrategy(readable=True, writable=True),
            ),
        )
    )
    assert isinstance(res, list) and len(res) > 0

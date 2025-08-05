from search_crawl_client import (
    BaseCrawlRequest,
    CacheStrategy,
    SearchCrawlRequest,
    SearchRequest,
)


def test_search_crawl(api):
    res = api.search_crawl(
        SearchCrawlRequest(
            search=SearchRequest(q="scraping test site"),
            crawl=BaseCrawlRequest(
                cache_strategy=CacheStrategy(readable=True, writable=True),
            ),
        )
    )
    assert isinstance(res, list) and len(res) > 0

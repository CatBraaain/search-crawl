import pytest

from search_crawl_client.models import (
    CacheStrategy,
    CrawlApiArg,
)


@pytest.mark.parametrize(
    "url, page_length",
    [
        ("https://example.com", 1),
        ("https://web-scraping.dev/products", 5),
        ("https://www.scrapethissite.com/pages/forms/?per_page=100", 6),
        ("https://quotes.toscrape.com/", 10),
    ],
)
def test_crawl_pagination(api, url, page_length):
    res = api.crawl(
        CrawlApiArg(
            url=url,
            cache_strategy=CacheStrategy(readable=True, writable=True),
        )
    )
    assert len(res) == page_length

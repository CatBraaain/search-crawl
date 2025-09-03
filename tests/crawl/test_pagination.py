import pytest

from search_crawl_client import (
    CacheConfig,
    CrawlRequest,
    DefaultApi,
)


def pagination_param(url: str, page: int):
    return pytest.param(url, page, id=f"[crawl {page} paginations]")


@pytest.mark.parametrize(
    ("url", "page_length"),
    [
        pagination_param("https://example.com", 1),
        pagination_param("https://web-scraping.dev/products", 5),
        pagination_param("https://www.scrapethissite.com/pages/forms/?per_page=100", 6),
        pagination_param("https://quotes.toscrape.com/", 10),
    ],
)
async def test_crawl_pagination(
    api: DefaultApi,
    url: str,
    page_length: int,
    cache_config: CacheConfig,
):
    res = await api.crawl(
        CrawlRequest(
            url=url,
            cache_config=cache_config,
        )
    )
    assert len(res) == page_length

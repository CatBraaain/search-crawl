import pytest

from search_crawl_client import (
    CacheConfig,
    CrawlConfig,
    CrawlRequestWithUrl,
    CrawlScope,
    DefaultApi,
)
from tests.conftest import TestSite


@pytest.mark.parametrize(
    ("url", "max_depth", "expected_page_length"),
    [
        (TestSite.QUOTES, 1, 2),
        (TestSite.QUOTES, 3, 4),
        (TestSite.QUOTES, None, 10),
    ],
)
async def test_crawl_max_depth(
    api: DefaultApi,
    url: str,
    max_depth: int,
    expected_page_length: int,
):
    res = await api.crawl(
        CrawlRequestWithUrl(
            url=url,
            crawl_config=CrawlConfig(
                crawl_scope=CrawlScope.PAGINATION,
                max_depth=max_depth,
            ),
            cache_config=CacheConfig(),
        )
    )
    assert len(res) == expected_page_length


@pytest.mark.parametrize(
    ("url", "max_pages", "expected_page_length"),
    [
        (TestSite.QUOTES, 1, 1),
        (TestSite.QUOTES, 3, 3),
        (TestSite.QUOTES, None, 10),
    ],
)
async def test_crawl_max_pages(
    api: DefaultApi,
    url: str,
    max_pages: int,
    expected_page_length: int,
):
    res = await api.crawl(
        CrawlRequestWithUrl(
            url=url,
            crawl_config=CrawlConfig(
                crawl_scope=CrawlScope.PAGINATION,
                max_depth=None,
                max_pages=max_pages,
            ),
            cache_config=CacheConfig(),
        )
    )
    assert len(res) == expected_page_length


@pytest.mark.parametrize(
    ("url", "scope", "expected_page_length"),
    [
        (TestSite.EXAMPLE, CrawlScope.PAGINATION, 1),
        (TestSite.EXAMPLE, CrawlScope.INTERNAL, 1),
        (TestSite.EXAMPLE, CrawlScope.ALL, 2),
        (TestSite.COUNTRY, CrawlScope.PAGINATION, 1),
        (TestSite.COUNTRY, CrawlScope.INTERNAL, 6),
        (TestSite.COUNTRY, CrawlScope.ALL, 7),
        (TestSite.PRODUCTS, CrawlScope.PAGINATION, 5),
        (TestSite.HOCKEY, CrawlScope.PAGINATION, 6),
    ],
)
async def test_crawl_scope(
    api: DefaultApi,
    url: str,
    scope: CrawlScope,
    expected_page_length: int,
):
    res = await api.crawl(
        CrawlRequestWithUrl(
            url=url,
            crawl_config=CrawlConfig(crawl_scope=scope),
            cache_config=CacheConfig(),
        )
    )
    assert len(res) == expected_page_length

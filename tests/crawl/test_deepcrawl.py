import pytest

from search_crawl_client import (
    CacheConfig,
    CrawlConfig,
    CrawlRequestWithUrl,
    CrawlScope,
    DefaultApi,
)
from tests.conftest import SiteEnum


@pytest.mark.parametrize(
    ("url", "max_depth", "expected_page_length"),
    [
        (SiteEnum.QUOTES, 1, 2),
        (SiteEnum.QUOTES, 3, 4),
        (SiteEnum.QUOTES, None, 10),
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
        (SiteEnum.QUOTES, 1, 1),
        (SiteEnum.QUOTES, 3, 3),
        (SiteEnum.QUOTES, None, 10),
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
        (SiteEnum.EXAMPLE, CrawlScope.PAGINATION, 1),
        (SiteEnum.EXAMPLE, CrawlScope.INTERNAL, 1),
        (SiteEnum.EXAMPLE, CrawlScope.ALL, 2),
        (SiteEnum.COUNTRY, CrawlScope.PAGINATION, 1),
        (SiteEnum.COUNTRY, CrawlScope.INTERNAL, 6),
        (SiteEnum.COUNTRY, CrawlScope.ALL, 7),
        (SiteEnum.PRODUCTS, CrawlScope.PAGINATION, 5),
        (SiteEnum.HOCKEY, CrawlScope.PAGINATION, 6),
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

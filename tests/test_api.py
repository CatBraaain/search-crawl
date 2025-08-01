import pytest
from fastapi.testclient import TestClient

from search_crawl.main import app
from search_crawl.routers.crawl import CacheStrategy, CrawlApiArg, CrawlManyApiArg


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_crawl(client):
    res = client.post(
        "/crawl",
        json=CrawlApiArg(
            url="https://example.com",
            cache_strategy=CacheStrategy(readable=False, writable=False),
        ).model_dump(),
    )
    assert res.json()


def test_crawl_pagination(client):
    res = client.post(
        "/crawl",
        json=CrawlApiArg(
            url="https://web-scraping.dev/products",
            cache_strategy=CacheStrategy(readable=False, writable=False),
        ).model_dump(),
    )
    assert len(res.json()) == 5

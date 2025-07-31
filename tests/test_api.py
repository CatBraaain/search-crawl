import pytest
from fastapi.testclient import TestClient

from search_crawl.crawl.scraper import CacheStrategy
from search_crawl.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_crawl(client):
    res = client.post(
        "/crawl",
        params={
            "url": "https://example.com",
            "cache_strategy": CacheStrategy(readable=False, writable=False),
        },
    )
    assert res.json()


def test_crawl_pagination(client):
    res = client.post(
        "/crawl",
        params={
            "url": "https://web-scraping.dev/products",
            "cache_strategy": CacheStrategy(readable=False, writable=False),
        },
    )
    assert len(res.json()) == 5

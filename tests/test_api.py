import pytest
from fastapi.testclient import TestClient

from search_crawl.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_crawl(client):
    res = client.get(
        "/crawl",
        params={"url": "https://example.com"},
    )
    assert res.json()


def test_crawl_pagination(client):
    res = client.get(
        "/crawl",
        params={"url": "https://web-scraping.dev/products"},
    )
    assert len(res.json()) == 5

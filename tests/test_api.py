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
        params={
            "urls": [
                "https://example.com",
                "https://example.net",
                "https://example.org",
            ]
        },
    )
    assert res.content


# def test_scrape(client):
#     urls = [
#         "https://example.com",
#         "https://example.net",
#         "https://example.org",
#     ]

#     res = client.get("/scrape", params={"urls": urls})
#     assert res.content

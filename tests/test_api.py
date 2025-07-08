from fastapi.testclient import TestClient

from search_crawl.main import app

client = TestClient(app)


def test_read_main():
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

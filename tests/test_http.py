from search_crawl_client import ApiClient, Configuration
from search_crawl_client.api.default_api import DefaultApi

config = Configuration(host="http://localhost:8000")
with ApiClient(config) as client:
    api = DefaultApi(client)


def test_healthz():
    res = api.healthz()
    assert res == "OK"


def test_search_general():
    res = api.search_general(q="ping")
    assert isinstance(res, list) and len(res) > 0


def test_search_images():
    res = api.search_images(q="ping")
    assert isinstance(res, list) and len(res) > 0


def test_crawl():
    res = api.crawl(url="https://example.com")
    assert res


def test_crawl_pagination():
    res = api.crawl(url="https://web-scraping.dev/products")
    print([r.url for r in res])
    assert len(res) == 5

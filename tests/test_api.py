import httpx


def test_healthz():
    res = httpx.get("http://localhost:8000/healthz")
    assert res.status_code == 200


def test_search_general():
    res = httpx.get("http://localhost:8000/search/general", params={"q": "ping"})
    assert res.status_code == 200
    assert isinstance(res.json(), list) and len(res.json()) > 0


def test_search_images():
    res = httpx.get("http://localhost:8000/search/images", params={"q": "ping"})
    assert res.status_code == 200
    assert isinstance(res.json(), list) and len(res.json()) > 0

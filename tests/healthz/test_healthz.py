from search_crawl_client import DefaultApi


async def test_healthz(api: DefaultApi):
    res = await api.healthz()
    assert res == "OK"

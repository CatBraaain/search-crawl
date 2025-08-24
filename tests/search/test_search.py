from search_crawl_client import DefaultApi, GeneralSearchRequest, ImageSearchRequest


async def test_search_general(api: DefaultApi):
    res = await api.search_general(GeneralSearchRequest(q="ping"))
    assert isinstance(res, list) and len(res) > 0


async def test_search_images(api: DefaultApi):
    res = await api.search_images(ImageSearchRequest(q="ping"))
    assert isinstance(res, list) and len(res) > 0

from search_crawl_client import GeneralSearchRequest, ImageSearchRequest


def test_search_general(api):
    res = api.search_general(GeneralSearchRequest(q="ping"))
    assert isinstance(res, list) and len(res) > 0


def test_search_images(api):
    res = api.search_images(ImageSearchRequest(q="ping"))
    assert isinstance(res, list) and len(res) > 0

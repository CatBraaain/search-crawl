def test_search_general(api):
    res = api.search_general(q="ping")
    assert isinstance(res, list) and len(res) > 0


def test_search_images(api):
    res = api.search_images(q="ping")
    assert isinstance(res, list) and len(res) > 0

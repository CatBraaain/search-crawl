def test_healthz(api):
    res = api.healthz()
    assert res == "OK"

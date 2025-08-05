from typing import Generator

import pytest

from search_crawl_client import ApiClient, Configuration, DefaultApi


@pytest.fixture
def api() -> Generator[DefaultApi, None, None]:
    config = Configuration(host="http://localhost:8000")
    with ApiClient(config) as client:
        yield DefaultApi(client)

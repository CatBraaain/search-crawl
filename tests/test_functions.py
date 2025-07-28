from unittest.mock import AsyncMock, patch

import pytest

from search_crawl.main import search_general, search_images


def get_param_set():
    default = {
        "language": "en",
        "page": 1,
        "time_range": None,
        "format": "json",
    }
    inputs = [
        {},
        {
            "language": "ja",
            "page": 2,
        },
        {
            "language": "all",
            "page": 3,
            "time_range": "day",
        },
    ]
    examples = [[input, {**default, **input}] for input in inputs]
    return examples


@pytest.mark.asyncio
@pytest.mark.parametrize("input, expected", get_param_set())
@patch("search_crawl.main.search", new_callable=AsyncMock)
async def test_arguments(mock_search: AsyncMock, input: dict, expected: dict):
    query = "query"
    await search_general(query, **input)
    mock_search.assert_awaited_with(
        q=query, engine_type="general", **{**input, **expected}
    )
    await search_images(query, **expected)
    mock_search.assert_awaited_with(
        q=query, engine_type="images", **{**input, **expected}
    )

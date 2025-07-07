from unittest.mock import AsyncMock, patch

import pytest

from search_crawl.main import search_general, search_images


class ArgsPattern:
    default = {
        "language": "ja",
        "page": 1,
        "time_range": None,
        "format": "json",
    }
    examples = [
        {},
        {
            "language": "en",
            "page": 2,
        },
        {
            "language": "all",
            "page": 3,
            "time_range": "day",
        },
    ]


@pytest.fixture
def args_pattern() -> ArgsPattern:
    return ArgsPattern()


@pytest.mark.asyncio
@patch("search_crawl.main.search", new_callable=AsyncMock)
async def test_arguments(mock_search: AsyncMock, args_pattern: ArgsPattern):
    query = "query"
    for example in args_pattern.examples:
        await search_general(query, **example)
        mock_search.assert_awaited_with(
            q=query, engine_type="general", **{**args_pattern.default, **example}
        )
        await search_images(query, **example)
        mock_search.assert_awaited_with(
            q=query, engine_type="images", **{**args_pattern.default, **example}
        )

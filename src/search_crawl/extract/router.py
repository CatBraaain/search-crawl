import json
from typing import Any, cast

import litellm
from fastapi import APIRouter
from litellm import ModelResponse, acompletion

from search_crawl.crawl.router import (
    CrawlRequestWithUrls,
    crawl,
    crawl_many,
)
from search_crawl.search.router import search

from .schemas import (
    CrawledContent,
    CrawlExtractRequest,
    ExtractRequest,
    SearchCrawlExtractRequest,
)

litellm.enable_json_schema_validation = True


router = APIRouter()


@router.post("/search-crawl-extract")
async def search_crawl_extract(
    req: SearchCrawlExtractRequest,
) -> dict[str, Any]:
    search_results = await search(req.search)
    crawl_results = await crawl_many(
        CrawlRequestWithUrls(
            **req.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return await extract_from_crawled_content(req.extract, crawl_results)


@router.post("/crawl-extract")
async def crawl_extract(
    req: CrawlExtractRequest,
) -> dict[str, Any]:
    crawl_result = await crawl(req.crawl)
    return await extract_from_crawled_content(req.extract, crawl_result)


async def extract_from_crawled_content(
    extract_request: ExtractRequest,
    crawled_content: CrawledContent,
) -> dict[str, Any]:
    response = cast(
        ModelResponse,
        await acompletion(
            model=extract_request.model,
            messages=extract_request.make_prompt(crawled_content),
            response_format=extract_request.make_response_format(),
        ),
    )
    return json.loads(response["choices"][0]["message"].content)

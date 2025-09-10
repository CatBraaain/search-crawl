import json
from typing import Any, cast

import litellm
from fastapi import APIRouter, HTTPException
from litellm import ModelResponse, acompletion
from litellm.exceptions import APIError

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
) -> Any:  # noqa: ANN401
    search_results = await search(req.search)
    crawl_results = await crawl_many(
        CrawlRequestWithUrls(
            **req.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return await extract(req.extract, crawl_results)


@router.post("/crawl-extract")
async def crawl_extract(
    req: CrawlExtractRequest,
) -> Any:  # noqa: ANN401
    crawl_result = await crawl(req.crawl)
    return await extract(req.extract, crawl_result)


async def extract(
    extract_request: ExtractRequest,
    crawled_content: CrawledContent,
) -> Any:  # noqa: ANN401
    try:
        response = cast(
            ModelResponse,
            await acompletion(
                model=extract_request.model,
                api_key=extract_request.api_key,
                messages=extract_request.make_prompt(crawled_content),
                response_format=extract_request.make_response_format(),
                **(extract_request.model_extra or {}),
            ),
        )
        return json.loads(response["choices"][0]["message"].content)
    except Exception as e:
        if isinstance(e, APIError):
            code = getattr(e, "status_code", 500)
            raise HTTPException(status_code=code, detail=str(e)) from e
        raise HTTPException(status_code=500, detail=str(e)) from e

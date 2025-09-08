import os

import httpx
from fastapi import APIRouter

from .schemas import (
    SearchRequest,
    SearchResult,
)

router = APIRouter()


@router.post("/search")
async def search(
    req: SearchRequest,
) -> list[SearchResult]:
    results = await search_with_cache(req)
    return [SearchResult(**result) for result in results]


async def search_with_cache(
    req: SearchRequest,
) -> list[dict]:
    cached_search = req.cache_config.wrap_with_cache(
        cache_key=f"search:{req.cache_key}",
        func=searxng,
    )
    results = await cached_search(req)

    if req.max_results is not None:
        return results[: req.max_results]
    else:
        return results


async def searxng(
    req: SearchRequest,
) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            os.environ["SEARXNG_URL"] + "/search",
            params=req.searxng_request,
        )
        return response.json()["results"]

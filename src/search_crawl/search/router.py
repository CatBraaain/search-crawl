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
    search_request: SearchRequest,
) -> list[SearchResult]:
    results = await search_with_cache(search_request)
    return [SearchResult(**result) for result in results]


async def search_with_cache(
    search_request: SearchRequest,
) -> list[dict]:
    cached_search = search_request.cache_config.wrap_with_cache(
        cache_key=f"search:{search_request.cache_key}",
        func=searxng,
    )
    results = await cached_search(search_request)

    if search_request.max_results is not None:
        return results[: search_request.max_results]
    else:
        return results


async def searxng(
    search_request: SearchRequest,
) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            os.environ["SEARXNG_URL"] + "/search",
            params=search_request.searxng_request,
        )
        return response.json()["results"]

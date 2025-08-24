import httpx
from fastapi import APIRouter

from .schemas import (
    GeneralSearchRequest,
    GeneralSearchResult,
    ImageSearchRequest,
    ImageSearchResult,
    SearchRequest,
)

router = APIRouter()


@router.post("/search/general", response_model=list[GeneralSearchResult])
async def search_general(
    search_request: GeneralSearchRequest,
) -> list[GeneralSearchResult]:
    cached_search = search_request.cache_config.wrap_with_cache(
        cache_key=f"search:{search_request.cache_key}",
        func=search,
    )
    results = await cached_search(search_request)
    return [GeneralSearchResult(**result) for result in results]


@router.post("/search/images", response_model=list[ImageSearchResult])
async def search_images(
    search_request: ImageSearchRequest,
) -> list[ImageSearchResult]:
    cached_search = search_request.cache_config.wrap_with_cache(
        cache_key=f"search:{search_request.cache_key}",
        func=search,
    )
    results = await cached_search(search_request)
    return [ImageSearchResult(**result) for result in results]


async def search(
    search_request: SearchRequest,
) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://search-crawl-searxng:8080/search",
            params=search_request.searxng_request,
        )
        return response.json()["results"]

from fastapi import APIRouter

from .search import (
    GeneralSearchRequest,
    GeneralSearchResult,
    ImageSearchRequest,
    ImageSearchResult,
    search,
)

router = APIRouter()


@router.post("/search/general", response_model=list[GeneralSearchResult])
async def search_general(
    search_request: GeneralSearchRequest,
) -> list[GeneralSearchResult]:
    return await search(search_request)


@router.post("/search/images", response_model=list[ImageSearchResult])
async def search_images(
    search_request: ImageSearchRequest,
) -> list[ImageSearchResult]:
    return await search(search_request)

from typing import Annotated, Literal, Optional, overload

import httpx
from pydantic import BaseModel, BeforeValidator, PlainSerializer

from ..cache_config import CacheConfig


class SearchRequest(BaseModel):
    q: str
    language: str = "en"
    page: int = 1
    time_range: Optional[Literal["day", "month", "year"]] = None
    format: Literal["json", "csv", "rss"] = "json"
    cache_config: CacheConfig = CacheConfig()

    @property
    def searxng_request(self):
        return self.model_dump(exclude={"cache_config"})


class GeneralSearchRequest(SearchRequest):
    engines: Annotated[
        list[str],
        PlainSerializer(lambda x: ",".join(x), return_type=str),
    ] = [
        "brave",
        "duckduckgo",
        "google",
        "presearch",
        "startpage",
        "yahoo",
    ]


class ImageSearchRequest(SearchRequest):
    engines: Annotated[
        list[str],
        PlainSerializer(lambda x: ",".join(x), return_type=str),
    ] = [
        "bing images",
        "duckduckgo images",
        "google images",
        "startpage images",
    ]


class BaseSearchResult(BaseModel):
    url: str
    title: str
    content: Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]


class GeneralSearchResult(BaseSearchResult):
    thumbnail: Optional[str]


class ImageSearchResult(BaseSearchResult):
    img_src: str


@overload
async def search(search_request: GeneralSearchRequest) -> list[GeneralSearchResult]: ...


@overload
async def search(search_request: ImageSearchRequest) -> list[ImageSearchResult]: ...


async def search(
    search_request: GeneralSearchRequest | ImageSearchRequest,
) -> list[GeneralSearchResult] | list[ImageSearchResult]:
    search_with_cache = search_request.cache_config.wrap_with_cache(_search)
    return await search_with_cache(search_request)


async def _search(
    search_request: SearchRequest,
) -> list[GeneralSearchResult] | list[ImageSearchResult]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://searxng:8080/search",
            params=search_request.searxng_request,
        )
        results = response.json()["results"]

    if isinstance(search_request, GeneralSearchRequest):
        return [GeneralSearchResult(**result) for result in results]
    elif isinstance(search_request, ImageSearchRequest):
        return [ImageSearchResult(**result) for result in results]
    else:
        raise NotImplementedError

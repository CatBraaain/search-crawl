import json
from typing import Annotated, Any, Literal, Optional, overload

import httpx
from pydantic import BaseModel, BeforeValidator, PlainSerializer

from ..cache_config import CacheConfig

GeneralEngineName = Literal[
    "bing",
    "brave",
    "duckduckgo",
    "google",
    "mojeek",
    "mullvadleta",
    "mullvadleta brave",
    "presearch",
    "presearch videos",
    "qwant",
    "startpage",
    "wiby",
    "yahoo",
    "seznam",
    "goo",
    "naver",
]

ImageEngineName = Literal[
    "bing images",
    "duckduckgo images",
    "google images",
    "startpage images",
    "brave.images",
    "mojeek images",
    "presearch images",
    "qwant images",
]


class SearchRequest(BaseModel):
    q: str
    engines: Any
    language: str = "en"
    page: int = 1
    time_range: Optional[Literal["day", "month", "year"]] = None
    format: Literal["json", "csv", "rss"] = "json"
    cache_config: CacheConfig = CacheConfig()

    @property
    def searxng_request(self):
        return self.model_dump(exclude={"cache_config"})

    @property
    def cache_key(self):
        return json.dumps(
            self.model_dump(exclude={"cache_config"}),
            separators=(",", "="),
        )


class GeneralSearchRequest(SearchRequest):
    engines: Annotated[
        list[GeneralEngineName],
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
        list[ImageEngineName],
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
    cached_search = search_request.cache_config.wrap_with_cache(
        cache_key=f"search:{search_request.cache_key}",
        func=_search,
    )
    results = await cached_search(search_request)

    if isinstance(search_request, GeneralSearchRequest):
        return [GeneralSearchResult(**result) for result in results]
    elif isinstance(search_request, ImageSearchRequest):
        return [ImageSearchResult(**result) for result in results]
    else:
        raise NotImplementedError


async def _search(
    search_request: SearchRequest,
) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://searxng:8080/search",
            params=search_request.searxng_request,
        )
        return response.json()["results"]

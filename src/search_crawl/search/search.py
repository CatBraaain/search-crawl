from typing import Annotated, Literal, Optional, overload

import httpx
from pydantic import BaseModel, BeforeValidator


class SearchRequest(BaseModel):
    q: str
    language: str = "en"
    page: int = 1
    time_range: Optional[Literal["day", "month", "year"]] = None
    format: Literal["json", "csv", "rss"] = "json"


class GeneralSearchRequest(SearchRequest):
    # Use string instead of list because OpenAPI does not support default values for object types
    engines: str = ",".join(
        [
            "brave",
            "duckduckgo",
            "google",
            "presearch",
            "startpage",
            "yahoo",
        ]
    )


class ImageSearchRequest(SearchRequest):
    engines: str = ",".join(
        [
            "bing images",
            "duckduckgo images",
            "google images",
            "startpage images",
        ]
    )


class BaseSearchResult(BaseModel):
    url: str
    title: str
    content: Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]


class GeneralSearchResult(BaseSearchResult):
    thumbnail: Optional[str]


class ImageSearchResult(BaseSearchResult):
    img_src: str


@overload
async def search(search_param: GeneralSearchRequest) -> list[GeneralSearchResult]: ...


@overload
async def search(search_param: ImageSearchRequest) -> list[ImageSearchResult]: ...


async def search(
    search_param: GeneralSearchRequest | ImageSearchRequest,
) -> list[GeneralSearchResult] | list[ImageSearchResult]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://searxng:8080/search",
            params=search_param.model_dump(),
        )
        results = response.json()["results"]

    if isinstance(search_param, GeneralSearchRequest):
        return [GeneralSearchResult(**result) for result in results]
    elif isinstance(search_param, ImageSearchRequest):
        return [ImageSearchResult(**result) for result in results]
    else:
        raise NotImplementedError

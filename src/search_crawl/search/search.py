from typing import Annotated, Literal, Optional, overload

import httpx
from pydantic import BaseModel, BeforeValidator


class BaseSearchResult(BaseModel):
    url: str
    title: str
    content: Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]


class GeneralSearchResult(BaseSearchResult):
    thumbnail: Optional[str]


class ImageSearchResult(BaseSearchResult):
    img_src: str


EngineType = Literal["general", "images"]

engines_map: dict[EngineType, list[str]] = {
    "general": [
        "brave",
        "duckduckgo",
        "google",
        "presearch",
        "startpage",
        "yahoo",
    ],
    "images": [
        "bing images",
        "duckduckgo images",
        "google images",
        "startpage images",
    ],
}


@overload
async def search(
    *,
    q: str,
    engine_type: Literal["general"],
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> list[GeneralSearchResult]: ...


@overload
async def search(
    *,
    q: str,
    engine_type: Literal["images"],
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> list[ImageSearchResult]: ...


async def search(
    *,
    q: str,
    engine_type: EngineType,
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> list[GeneralSearchResult] | list[ImageSearchResult]:
    engines = engines_map[engine_type]
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://searxng:8080/search",
            params={
                "q": q,
                "engines": ",".join(engines),
                "language": language,
                "page": page,
                "time_range": time_range,
                "format": format,
            },
        )
        return response.json()["results"]

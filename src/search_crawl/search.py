import os
from typing import List, Literal, Optional, overload

import httpx
from typing_extensions import TypedDict


class GeneralSearchResult(TypedDict):
    url: str
    title: str
    content: str
    thumbnail: Optional[str]
    engine: str
    template: Literal["default.html", "videos.html", "images.html"]
    parsed_url: List[str]
    engines: List[str]
    score: float


class ImageSearchResult(TypedDict):
    img_src: str
    url: str
    title: str
    content: str
    engine: str
    template: Literal["default.html", "videos.html", "images.html"]
    parsed_url: List[str]
    engines: List[str]
    score: float


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
) -> List[GeneralSearchResult]: ...


@overload
async def search(
    *,
    q: str,
    engine_type: Literal["images"],
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> List[ImageSearchResult]: ...


async def search(
    *,
    q: str,
    engine_type: EngineType,
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> List[GeneralSearchResult] | List[ImageSearchResult]:
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

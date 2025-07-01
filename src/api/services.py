from typing import List, Literal, Optional, overload

import httpx
from schemas import GeneralSearchResult, ImageSearchResult

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
async def fetch_results(
    q: str,
    engine_type: Literal["general"],
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> List[GeneralSearchResult]: ...


@overload
async def fetch_results(
    q: str,
    engine_type: Literal["images"],
    language: Optional[str],
    page: int,
    time_range: Optional[Literal["day", "month", "year"]],
    format: Optional[Literal["json", "csv", "rss"]],
) -> List[ImageSearchResult]: ...


async def fetch_results(
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
            "http://localhost:8080/search",
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

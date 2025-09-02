import json
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, PlainSerializer

from search_crawl.cache_config import CacheConfig

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
    time_range: Literal["day", "month", "year"] | None = None
    format: Literal["json", "csv", "rss"] = "json"
    max_results: int | None = None
    cache_config: CacheConfig = CacheConfig()

    @property
    def searxng_request(self) -> dict[str, Any]:
        return self.model_dump(exclude={"max_results", "cache_config"})

    @property
    def cache_key(self) -> str:
        return json.dumps(
            self.model_dump(exclude={"max_results", "cache_config"}),
            separators=(",", "="),
        )


class GeneralSearchRequest(SearchRequest):
    engines: Annotated[
        list[GeneralEngineName],
        PlainSerializer(lambda x: ",".join(sorted(x)), return_type=str),
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
        PlainSerializer(lambda x: ",".join(sorted(x)), return_type=str),
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
    thumbnail: str | None


class ImageSearchResult(BaseSearchResult):
    img_src: str

import json
from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, PlainSerializer

from search_crawl.cache_config import CacheConfig


class EnginePresetKey(StrEnum):
    general = "GENERAL"
    image = "IMAGE"


ENGINE_PRESETS = {
    EnginePresetKey.general: [
        "brave",
        "duckduckgo",
        "google",
        "presearch",
        "startpage",
        "yahoo",
    ],
    EnginePresetKey.image: [
        "bing images",
        "duckduckgo images",
        "google images",
        "startpage images",
    ],
}


class SearchRequest(BaseModel):
    q: str
    engines: Annotated[
        list[str] | EnginePresetKey,
        PlainSerializer(
            lambda engines: ",".join(
                sorted(ENGINE_PRESETS[engines])
                if isinstance(engines, EnginePresetKey)
                else engines
            ),
            return_type=str,
        ),
    ] = EnginePresetKey.general
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
            ensure_ascii=False,
        )


class SearchResult(BaseModel):
    url: str
    title: str
    content: Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]
    img_src: Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]

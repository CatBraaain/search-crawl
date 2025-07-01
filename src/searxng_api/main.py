from typing import List, Literal, Optional

from fastapi import FastAPI
from .schemas import GeneralSearchResult, ImageSearchResult
from .services import fetch_results

app = FastAPI()


@app.get("/search/general", response_model=List[GeneralSearchResult])
async def search_general(
    q: str,
    language: Optional[str] = "ja",
    page: int = 1,
    time_range: Optional[Literal["day", "month", "year"]] = None,
    format: Optional[Literal["json", "csv", "rss"]] = "json",
) -> List[GeneralSearchResult]:
    return await fetch_results(q, "general", language, page, time_range, format)


@app.get("/search/images", response_model=List[ImageSearchResult])
async def search_images(
    q: str,
    language: Optional[str] = "ja",
    page: int = 1,
    time_range: Optional[Literal["day", "month", "year"]] = None,
    format: Optional[Literal["json", "csv", "rss"]] = "json",
) -> List[ImageSearchResult]:
    return await fetch_results(q, "images", language, page, time_range, format)

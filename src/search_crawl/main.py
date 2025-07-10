from contextlib import asynccontextmanager
from typing import Annotated, List, Literal, Optional

from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRoute

from .schemas import GeneralSearchResult, ImageSearchResult
from .scrape import Scraper, ScrapeResult
from .services import search

scraper: Scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scraper
    async with Scraper(
        i_know_what_im_doing=True,
        headless=True,
        block_images=True,
    ) as scraper:
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "OK"


@app.get("/search/general", response_model=List[GeneralSearchResult])
async def search_general(
    q: str,
    language: Optional[str] = "ja",
    page: int = 1,
    time_range: Optional[Literal["day", "month", "year"]] = None,
    format: Optional[Literal["json", "csv", "rss"]] = "json",
) -> List[GeneralSearchResult]:
    return await search(
        q=q,
        engine_type="general",
        language=language,
        page=page,
        time_range=time_range,
        format=format,
    )


@app.get("/search/images", response_model=List[ImageSearchResult])
async def search_images(
    q: str,
    language: Optional[str] = "ja",
    page: int = 1,
    time_range: Optional[Literal["day", "month", "year"]] = None,
    format: Optional[Literal["json", "csv", "rss"]] = "json",
) -> List[ImageSearchResult]:
    return await search(
        q=q,
        engine_type="images",
        language=language,
        page=page,
        time_range=time_range,
        format=format,
    )


@app.get("/crawl", response_model=list[list[ScrapeResult]])
async def crawl(urls: Annotated[list[str], Query()]) -> list[list[ScrapeResult]]:
    return [[]]
    # return await acrawl(urls)


@app.get("/scrape", response_model=list[ScrapeResult])
async def scrape(urls: Annotated[list[str], Query()]) -> list[ScrapeResult]:
    return await scraper.run(urls)


def simplify_client_method_names(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


simplify_client_method_names(app)

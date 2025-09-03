import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from patchright.async_api import async_playwright

from .crawler import Crawler, ScrapeResult
from .schemas import (
    BaseCrawlRequest,  # noqa: F401
    CrawlManyRequest,
    CrawlRequest,
)

crawler: Crawler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    global crawler  # noqa: PLW0603
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        crawler = Crawler(browser)
        yield


router = APIRouter(lifespan=lifespan)


@router.post("/crawl")
async def crawl(
    crawl_request: CrawlRequest,
) -> list[ScrapeResult]:
    sem = asyncio.Semaphore(crawl_request.concurrently)
    return await crawler.crawl(crawl_request.url, sem, crawl_request.cache_config)


@router.post("/crawl-many")
async def crawl_many(
    crawl_many_request: CrawlManyRequest,
) -> list[list[ScrapeResult]]:
    sem = asyncio.Semaphore(crawl_many_request.concurrently)
    return await asyncio.gather(
        *(
            crawler.crawl(url, sem, crawl_many_request.cache_config)
            for url in crawl_many_request.urls
        )
    )

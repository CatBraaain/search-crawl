import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from patchright.async_api import async_playwright

from .crawler import Crawler, ScrapeResult
from .schemas import (
    BaseCrawlRequest,  # pyright: ignore[reportUnusedImport]
    CrawlManyRequest,
    CrawlRequest,
)

crawler: Crawler


@asynccontextmanager
async def lifespan(app: FastAPI):
    global crawler
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        crawler = Crawler(browser)
        yield


router = APIRouter(lifespan=lifespan)


@router.post("/crawl", response_model=list[ScrapeResult])
async def crawl(
    crawl_request: CrawlRequest,
) -> list[ScrapeResult]:
    sem = asyncio.Semaphore(crawl_request.concurrently)
    return await crawler.crawl(crawl_request.url, sem, crawl_request.cache_config)


@router.post("/crawl-many", response_model=list[list[ScrapeResult]])
async def crawl_many(crawl_many_request: CrawlManyRequest) -> list[list[ScrapeResult]]:
    sem = asyncio.Semaphore(crawl_many_request.concurrently)
    return await asyncio.gather(
        *(
            crawler.crawl(url, sem, crawl_many_request.cache_config)
            for url in crawl_many_request.urls
        )
    )

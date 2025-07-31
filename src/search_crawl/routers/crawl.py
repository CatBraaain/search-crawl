import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from patchright.async_api import async_playwright

from ..crawl.crawler import CacheStrategy, Crawler, ScrapeResult

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
    url: str,
    cache_strategy: CacheStrategy = CacheStrategy(),
    concurrently: int = 2,
) -> list[ScrapeResult]:
    sem = asyncio.Semaphore(concurrently)
    return await crawler.crawl(url, sem, cache_strategy)

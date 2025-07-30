import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from patchright.async_api import Browser, async_playwright

from ..crawler import Crawler, ScrapeResult

browser: Browser


@asynccontextmanager
async def lifespan(app: FastAPI):
    global browser
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        yield


router = APIRouter(lifespan=lifespan)


@router.get("/crawl", response_model=list[ScrapeResult])
async def crawl(
    url: str, concurrently: int = 2, ttl: str = "24h"
) -> list[ScrapeResult]:
    sem = asyncio.Semaphore(concurrently)
    return await Crawler(browser).crawl(url, sem, ttl)

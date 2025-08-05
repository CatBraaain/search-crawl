import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from patchright.async_api import async_playwright
from pydantic import BaseModel

from .crawler import CacheStrategy, Crawler, ScrapeResult

crawler: Crawler


@asynccontextmanager
async def lifespan(app: FastAPI):
    global crawler
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        crawler = Crawler(browser)
        yield


router = APIRouter(lifespan=lifespan)


class BaseCrawlRequest(BaseModel):
    cache_strategy: CacheStrategy = CacheStrategy()
    concurrently: int = 2


class CrawlRequest(BaseCrawlRequest):
    url: str


class CrawlManyRequest(BaseCrawlRequest):
    urls: list[str]


@router.post("/crawl", response_model=list[ScrapeResult])
async def crawl(
    crawl_request: CrawlRequest,
) -> list[ScrapeResult]:
    sem = asyncio.Semaphore(crawl_request.concurrently)
    return await crawler.crawl(crawl_request.url, sem, crawl_request.cache_strategy)


@router.post("/crawl-many", response_model=list[list[ScrapeResult]])
async def crawl_many(crawl_many_request: CrawlManyRequest) -> list[list[ScrapeResult]]:
    sem = asyncio.Semaphore(crawl_many_request.concurrently)
    return await asyncio.gather(
        *(
            crawler.crawl(url, sem, crawl_many_request.cache_strategy)
            for url in crawl_many_request.urls
        )
    )

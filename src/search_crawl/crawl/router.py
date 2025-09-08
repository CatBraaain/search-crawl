import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from patchright.async_api import async_playwright

from search_crawl.search.router import search

from .crawler import Crawler, ScrapeResult
from .schemas import (
    BaseCrawlRequest,  # noqa: F401
    CrawlManyRequest,
    CrawlRequest,
    SearchCrawlRequest,
    SearchCrawlResult,
)

router = APIRouter()


crawler: Crawler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    global crawler  # noqa: PLW0603
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        crawler = Crawler(browser)
        yield


router = APIRouter(lifespan=lifespan)


@router.post("/crawl")
async def crawl(
    req: CrawlRequest,
) -> list[ScrapeResult]:
    sem = asyncio.Semaphore(req.concurrently)
    return await crawler.crawl(req.url, sem, req.cache_config)


@router.post("/crawl-many")
async def crawl_many(
    req: CrawlManyRequest,
) -> list[list[ScrapeResult]]:
    sem = asyncio.Semaphore(req.concurrently)
    return await asyncio.gather(
        *(crawler.crawl(url, sem, req.cache_config) for url in req.urls)
    )


@router.post("/search-crawl")
async def search_crawl(
    req: SearchCrawlRequest,
) -> list[SearchCrawlResult]:
    search_results = await search(req.search)
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **req.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return [
        SearchCrawlResult(search=search_result, crawl=crawl_result)
        for search_result, crawl_result in zip(
            search_results, crawl_results, strict=True
        )
    ]

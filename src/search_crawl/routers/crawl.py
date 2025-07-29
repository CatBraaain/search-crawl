from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from ..crawler import CrawlerService, ScrapeResult

crawler_service: CrawlerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    global crawler_service
    async with CrawlerService(
        i_know_what_im_doing=True,
        headless=True,
        block_images=True,
    ) as crawler_service:
        yield


router = APIRouter(lifespan=lifespan)


@router.get("/crawl", response_model=list[ScrapeResult])
async def crawl(
    url: str, concurrently: int = 2, ttl: str = "24h"
) -> list[ScrapeResult]:
    return await crawler_service.launch_crawl(url, concurrently=concurrently, ttl=ttl)

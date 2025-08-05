from typing import Literal, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ..crawl.routing import BaseCrawlRequest, CrawlManyRequest, ScrapeResult, crawl_many
from ..search.search import search

router = APIRouter()


class SearchRequest(BaseModel):
    q: str
    language: Optional[str] = "en"
    page: int = 1
    time_range: Optional[Literal["day", "month", "year"]] = None
    format: Optional[Literal["json", "csv", "rss"]] = "json"


class SearchCrawlRequest(BaseModel):
    search: SearchRequest
    crawl: BaseCrawlRequest = BaseCrawlRequest()


@router.post("/search-crawl", response_model=list[list[ScrapeResult]])
async def search_crawl(
    search_crawl_request: SearchCrawlRequest,
) -> list[list[ScrapeResult]]:
    search_results = await search(
        **search_crawl_request.search.model_dump(),
        engine_type="general",
    )
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **search_crawl_request.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return crawl_results

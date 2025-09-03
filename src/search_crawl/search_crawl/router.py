from fastapi import APIRouter

from search_crawl.crawl.router import CrawlManyRequest, crawl_many
from search_crawl.search.router import (
    search,
)

from .schemas import (
    SearchCrawlRequest,
    SearchCrawlResult,
)

router = APIRouter()


@router.post("/search-crawl")
async def crawl_search(
    param: SearchCrawlRequest,
) -> list[SearchCrawlResult]:
    search_results = await search(param.search)
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **param.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return [
        SearchCrawlResult(search=search_result, crawl=crawl_result)
        for search_result, crawl_result in zip(
            search_results, crawl_results, strict=True
        )
    ]

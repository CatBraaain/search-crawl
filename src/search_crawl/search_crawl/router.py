from fastapi import APIRouter
from pydantic import BaseModel

from ..crawl.router import BaseCrawlRequest, CrawlManyRequest, ScrapeResult, crawl_many
from ..search.search import (
    GeneralSearchRequest,
    GeneralSearchResult,
    ImageSearchRequest,
    ImageSearchResult,
    search,
)

router = APIRouter()


class BaseSearchCrawlRequest(BaseModel):
    crawl: BaseCrawlRequest = BaseCrawlRequest()


class GeneralSearchCrawlRequest(BaseSearchCrawlRequest):
    search: GeneralSearchRequest


class ImageSearchCrawlRequest(BaseSearchCrawlRequest):
    search: ImageSearchRequest


class GeneralSearchCrawlResult(BaseModel):
    search: GeneralSearchResult
    crawl: list[ScrapeResult]


class ImageSearchCrawlResult(BaseModel):
    search: ImageSearchResult
    crawl: list[ScrapeResult]


@router.post("/search-crawl/general", response_model=list[GeneralSearchCrawlResult])
async def crawl_search_general(
    param: GeneralSearchCrawlRequest,
) -> list[GeneralSearchCrawlResult]:
    search_results = await search(param.search)
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **param.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return [
        GeneralSearchCrawlResult(search=search_result, crawl=crawl_result)
        for search_result, crawl_result in zip(search_results, crawl_results)
    ]


@router.post("/search-crawl/image", response_model=list[ImageSearchCrawlResult])
async def crawl_search_image(
    param: ImageSearchCrawlRequest,
) -> list[ImageSearchCrawlResult]:
    search_results = await search(param.search)
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **param.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return [
        ImageSearchCrawlResult(search=search_result, crawl=crawl_result)
        for search_result, crawl_result in zip(search_results, crawl_results)
    ]

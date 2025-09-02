from fastapi import APIRouter

from search_crawl.crawl.router import CrawlManyRequest, crawl_many
from search_crawl.search.router import (
    search_general,
    search_images,
)

from .schemas import (
    GeneralSearchCrawlRequest,
    GeneralSearchCrawlResult,
    ImageSearchCrawlRequest,
    ImageSearchCrawlResult,
)

router = APIRouter()


@router.post("/search-crawl/general")
async def crawl_search_general(
    param: GeneralSearchCrawlRequest,
) -> list[GeneralSearchCrawlResult]:
    search_results = await search_general(param.search)
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **param.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return [
        GeneralSearchCrawlResult(search=search_result, crawl=crawl_result)
        for search_result, crawl_result in zip(
            search_results, crawl_results, strict=True
        )
    ]


@router.post("/search-crawl/image")
async def crawl_search_image(
    param: ImageSearchCrawlRequest,
) -> list[ImageSearchCrawlResult]:
    search_results = await search_images(param.search)
    crawl_results = await crawl_many(
        CrawlManyRequest(
            **param.crawl.model_dump(),
            urls=[search_result.url for search_result in search_results],
        )
    )
    return [
        ImageSearchCrawlResult(search=search_result, crawl=crawl_result)
        for search_result, crawl_result in zip(
            search_results, crawl_results, strict=True
        )
    ]

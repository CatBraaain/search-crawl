from fastapi import APIRouter

from ..crawl.router import CrawlManyRequest, crawl_many
from ..search.router import (
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


@router.post("/search-crawl/general", response_model=list[GeneralSearchCrawlResult])
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
        for search_result, crawl_result in zip(search_results, crawl_results)
    ]


@router.post("/search-crawl/image", response_model=list[ImageSearchCrawlResult])
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
        for search_result, crawl_result in zip(search_results, crawl_results)
    ]

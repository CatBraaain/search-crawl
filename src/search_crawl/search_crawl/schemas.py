from pydantic import BaseModel

from ..crawl.router import BaseCrawlRequest, ScrapeResult
from ..search.router import (
    GeneralSearchRequest,
    GeneralSearchResult,
    ImageSearchRequest,
    ImageSearchResult,
)


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

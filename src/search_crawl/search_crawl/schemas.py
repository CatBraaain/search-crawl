from pydantic import BaseModel

from search_crawl.crawl.router import BaseCrawlRequest, ScrapeResult
from search_crawl.search.router import (
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

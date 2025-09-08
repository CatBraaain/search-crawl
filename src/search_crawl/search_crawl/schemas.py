from pydantic import BaseModel

from search_crawl.crawl.router import BaseCrawlRequest, ScrapeResult
from search_crawl.search.router import (
    SearchRequest,
    SearchResult,
)


class SearchCrawlRequest(BaseModel):
    search: SearchRequest
    crawl: BaseCrawlRequest = BaseCrawlRequest()


class SearchCrawlResult(BaseModel):
    search: SearchResult
    crawl: list[ScrapeResult]

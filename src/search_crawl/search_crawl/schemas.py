from pydantic import BaseModel

from search_crawl.crawl.router import BaseCrawlRequest, ScrapeResult
from search_crawl.search.router import (
    SearchRequest,
    SearchResult,
)


class SearchCrawlRequest(BaseModel):
    crawl: BaseCrawlRequest = BaseCrawlRequest()
    search: SearchRequest


class SearchCrawlResult(BaseModel):
    search: SearchResult
    crawl: list[ScrapeResult]

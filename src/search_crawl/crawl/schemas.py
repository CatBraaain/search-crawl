from pydantic import BaseModel

from search_crawl.cache_config import CacheConfig
from search_crawl.search.router import (
    SearchRequest,
    SearchResult,
)


class BaseCrawlRequest(BaseModel):
    cache_config: CacheConfig = CacheConfig()
    concurrently: int = 2


class CrawlRequest(BaseCrawlRequest):
    url: str


class CrawlManyRequest(BaseCrawlRequest):
    urls: list[str]


class ScrapeResult(BaseModel):
    requested_url: str
    url: str
    title: str
    short_title: str
    author: str
    html: str
    markdown: str
    summary_html: str
    summary_md: str
    links: list[str]
    pagination_links: list[str]


class SearchCrawlRequest(BaseModel):
    search: SearchRequest
    crawl: BaseCrawlRequest = BaseCrawlRequest()


class SearchCrawlResult(BaseModel):
    search: SearchResult
    crawl: list[ScrapeResult]

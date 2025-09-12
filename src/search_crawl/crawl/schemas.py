from enum import StrEnum, auto

from pydantic import BaseModel

from search_crawl.cache_config import CacheConfig
from search_crawl.search.router import (
    SearchRequest,
    SearchResult,
)


class CrawlScope(StrEnum):
    PAGINATION = auto()
    INTERNAL = auto()
    ALL = auto()


class OutputFormat(StrEnum):
    FULL_MARKDOWN = auto()
    MAIN_MARKDOWN = auto()
    FULL_HTML = auto()
    MAIN_HTML = auto()


class CrawlConfig(BaseModel):
    crawl_scope: CrawlScope = CrawlScope.PAGINATION
    max_depth: int | None = 1
    max_pages: int | None = None
    concurrently: int = 2
    output_format: OutputFormat = OutputFormat.MAIN_MARKDOWN


class CrawlRequest(BaseModel):
    crawl_config: CrawlConfig = CrawlConfig()
    cache_config: CacheConfig = CacheConfig()


class CrawlRequestWithUrl(CrawlRequest):
    url: str


class CrawlRequestWithUrls(CrawlRequest):
    urls: list[str]


class ScrapeResult(BaseModel):
    requested_url: str
    url: str
    title: str
    short_title: str
    author: str
    content: str
    links: list[str]
    internal_links: list[str]
    pagination_links: list[str]


class SearchCrawlRequest(BaseModel):
    search: SearchRequest
    crawl: CrawlRequest = CrawlRequest()


class SearchCrawlResult(BaseModel):
    search: SearchResult
    crawl: list[ScrapeResult]

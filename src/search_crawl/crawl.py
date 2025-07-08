import re
from typing import TypedDict, cast
from urllib.parse import urlparse, urlunparse

from crawl4ai import (
    AsyncWebCrawler,
    BFSDeepCrawlStrategy,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    CrawlResult,
    FilterChain,
    URLPatternFilter,
)


class Media(TypedDict):
    images: list[str]
    videos: list[str]
    audios: list[str]


class Image(TypedDict):
    src: str
    alt: str
    desc: str


class Link(TypedDict):
    href: str
    text: str
    title: str
    base_domain: str


class ScrapeResult(TypedDict):
    url: str
    html: str
    links: list[Link]
    images: list[Image]
    markdown: str
    metadata: dict


async def acrawl(urls) -> list[list[ScrapeResult]]:
    config = Config(urls)
    async with AsyncWebCrawler(config=config.browser) as crawler:
        results_list = [await crawler.arun(url, config=config.crawler) for url in urls]
        results_list = cast(list[list[list[CrawlResult]]], results_list)
        results_list = [
            [convert_result(bfs_result[0]) for bfs_result in results]
            for results in results_list
        ]
        return results_list


def convert_result(crawl_result: CrawlResult) -> ScrapeResult:
    scrape_result = {
        "html": crawl_result.html,
        "markdown": crawl_result.markdown,
        "links": crawl_result.links["internal"] + crawl_result.links["external"],
        "images": [
            {k: image[k] for k in ["src", "alt", "desc"]}
            for image in crawl_result.media["images"]
        ],
        "metadata": crawl_result.metadata,
        "url": crawl_result.url,
    }
    return cast(ScrapeResult, scrape_result)


class Config:
    browser: BrowserConfig
    crawler: CrawlerRunConfig

    def __init__(self, urls: list[str]) -> None:
        self.browser = BrowserConfig(
            viewport_width=1920,
            viewport_height=1080,
            user_agent_mode="random",
            light_mode=True,
            text_mode=True,
        )
        self.crawler = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            # cache_mode=CacheMode.WRITE_ONLY,
            remove_overlay_elements=True,
            simulate_user=True,
            magic=True,
            override_navigator=True,
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=2,
                max_pages=10,
                filter_chain=FilterChain(
                    [URLPatternFilter([self.paged_url_regex(url) for url in urls])]
                ),
            ),
        )

    def paged_url_regex(self, url) -> re.Pattern[str]:
        parsed = urlparse(url)
        base_url = urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path.removesuffix("/"), "", "", "")
        )
        paging_pattern = r".*\b(p|page)\b.?\d{1,2}.*"
        return re.compile(rf"{re.escape(base_url)}{paging_pattern}")

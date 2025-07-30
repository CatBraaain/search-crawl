import asyncio
from typing import Any, Self

from camoufox.async_api import AsyncCamoufox, Browser, BrowserContext
from cashews import cache

from .scraper import URL, Scraper, ScrapeResult

cache.setup("disk://?directory=.cache&shards=0")


class Crawler:
    scraper: Scraper
    visited: list[URL]
    results: list[ScrapeResult]

    def __init__(
        self,
        browser: Browser | BrowserContext,
        ttl: str = "24h",
    ) -> None:
        self.scraper = Scraper(browser)
        self.visited = []
        self.results = []
        self.ttl = ttl

    async def crawl(
        self,
        requested_url: str,
        sem: asyncio.Semaphore,
    ) -> list[ScrapeResult]:
        if requested_url in self.visited:
            return []
        else:
            self.visited.append(URL(requested_url))

        async with sem:
            scrape_result = await self.scraper.scrape(requested_url, self.ttl)
            self.results.append(scrape_result)

        await asyncio.gather(
            *[
                self.crawl(pagination_link, sem)
                for pagination_link in scrape_result["pagination_links"]
            ]
        )

        return self.results


class CrawlerService:
    camoufox: AsyncCamoufox
    camoufox_options: dict[str, Any]
    browser: Browser | BrowserContext

    def __init__(self, **camoufox_options) -> None:
        self.camoufox_options = camoufox_options

    async def __aenter__(self) -> Self:
        self.camoufox = AsyncCamoufox(**self.camoufox_options)
        self.browser = await self.camoufox.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.camoufox.__aexit__(exc_type, exc_val, exc_tb)

    async def launch_crawl(
        self, requested_url: str, concurrently: int, ttl: str
    ) -> list[ScrapeResult]:
        crawler = Crawler(self.browser, ttl)
        # workaround for Camoufox freezing when opening multiple pages concurrently
        # see: https://github.com/daijro/camoufox/issues/279
        concurrently = 2
        sem = asyncio.Semaphore(concurrently)
        return await crawler.crawl(requested_url, sem)

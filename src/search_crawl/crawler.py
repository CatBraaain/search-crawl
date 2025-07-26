import asyncio
from typing import Any, Self

from camoufox.async_api import AsyncCamoufox, Browser, BrowserContext
from cashews import cache
from markitdown import MarkItDown

from .scraper import URL, Navigation, Readable, ScrapeResult

cache.setup("disk://?directory=.cache&shards=0")


class Crawler:
    browser: Browser | BrowserContext
    markitdown: MarkItDown
    visited: list[URL]
    results: list[ScrapeResult]

    def __init__(
        self, browser: Browser | BrowserContext, markitdown: MarkItDown
    ) -> None:
        self.browser = browser
        self.markitdown = markitdown
        self.visited = []
        self.results = []

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
            scrape_result = await self.scrape(requested_url)
            self.results.append(scrape_result)

        await asyncio.gather(
            *[
                self.crawl(pagination_link, sem)
                for pagination_link in scrape_result["pagination_links"]
            ]
        )

        return self.results

    async def scrape(self, requested_url: str) -> ScrapeResult:
        url, raw_html = await self.scrape_raw(requested_url)

        readable = Readable(raw_html, self.markitdown)
        navigation = Navigation(raw_html, url)

        return {
            "requested_url": requested_url,
            "url": str(url),
            "title": readable.title(),
            "short_title": readable.short_title(),
            "author": readable.author(),
            "html": raw_html,
            "content": readable.content(),
            "summary_html": readable.summary_html(),
            "summary_md": readable.summary_md(),
            "links": navigation.links,
            "pagination_links": navigation.pagination_links,
        }

    @cache(ttl="24h", key="{requested_url}")
    async def scrape_raw(self, requested_url: str) -> tuple[URL, str]:
        page = await self.browser.new_page()
        await page.goto(requested_url, timeout=10000, wait_until="load")
        raw_html = await page.content()
        await page.close()
        return URL(page.url), raw_html


class CrawlerService:
    camoufox: AsyncCamoufox
    camoufox_options: dict[str, Any]
    browser: Browser | BrowserContext
    markitdown: MarkItDown

    def __init__(self, **camoufox_options) -> None:
        self.camoufox_options = camoufox_options
        self.markitdown = MarkItDown()

    async def __aenter__(self) -> Self:
        self.camoufox = AsyncCamoufox(**self.camoufox_options)
        self.browser = await self.camoufox.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.camoufox.__aexit__(exc_type, exc_val, exc_tb)

    async def crawl(self, requested_url: str) -> list[ScrapeResult]:
        crawler = Crawler(self.browser, self.markitdown)
        # workaround for Camoufox freezing when opening multiple pages concurrently
        # see: https://github.com/daijro/camoufox/issues/279
        sem = asyncio.Semaphore(1)
        return await crawler.crawl(requested_url, sem)

import asyncio

from patchright.async_api import Browser

from .scraper import URL, Scraper, ScrapeResult


class Crawler:
    scraper: Scraper
    visited: list[URL]
    results: list[ScrapeResult]

    def __init__(
        self,
        browser: Browser,
    ) -> None:
        self.scraper = Scraper(browser)
        self.visited = []
        self.results = []

    async def crawl(
        self,
        requested_url: str,
        sem: asyncio.Semaphore,
        ttl: str = "24h",
    ) -> list[ScrapeResult]:
        if requested_url in self.visited:
            return []
        else:
            self.visited.append(URL(requested_url))

        async with sem:
            scrape_result = await self.scraper.scrape(requested_url, ttl)
            self.results.append(scrape_result)

        await asyncio.gather(
            *[
                self.crawl(pagination_link, sem, ttl)
                for pagination_link in scrape_result["pagination_links"]
            ]
        )

        return self.results

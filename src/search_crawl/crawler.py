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

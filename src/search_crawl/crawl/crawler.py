import asyncio

from patchright.async_api import Browser

from .scraper import URL, Scraper, ScrapeResult


class Crawler:
    scraper: Scraper

    def __init__(
        self,
        browser: Browser,
    ) -> None:
        self.scraper = Scraper(browser)

    async def crawl(
        self,
        requested_url: str,
        sem: asyncio.Semaphore,
        ttl: str = "24h",
    ) -> list[ScrapeResult]:
        visited: list[URL] = []
        results: list[ScrapeResult] = []

        async def _crawl(_url: str) -> None:
            if _url in visited:
                return
            visited.append(URL(_url))

            async with sem:
                result = await self.scraper.scrape(_url, ttl)
                results.append(result)

            await asyncio.gather(
                *[
                    _crawl(pagination_link)
                    for pagination_link in result["pagination_links"]
                ]
            )

        await _crawl(requested_url)
        return results

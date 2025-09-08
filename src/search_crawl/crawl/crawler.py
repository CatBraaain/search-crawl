import asyncio

from patchright.async_api import Browser, Error as PlaywrightError

from search_crawl.cache_config import CacheConfig

from .schemas import ScrapeResult
from .utils import URL, Navigation, Readable


class Crawler:
    browser: Browser

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    async def crawl(
        self,
        requested_url: str,
        sem: asyncio.Semaphore,
        cache_config: CacheConfig,
    ) -> list[ScrapeResult]:
        visited: list[URL] = []
        results: list[ScrapeResult] = []

        async def _crawl(_url: str) -> None:
            if _url in visited:
                return
            visited.append(URL(_url))

            async with sem:
                result = await self.scrape(_url, cache_config)
                results.append(result)

            await asyncio.gather(
                *[
                    _crawl(pagination_link)
                    for pagination_link in result.pagination_links
                ]
            )

        await _crawl(requested_url)
        return results

    async def scrape(
        self, requested_url: str, cache_config: CacheConfig
    ) -> ScrapeResult:
        scrape_with_cache = cache_config.wrap_with_cache(
            cache_key=f"scrape:{requested_url}",
            func=self.scrape_raw,
        )
        url_str, raw_html = await scrape_with_cache(requested_url)
        url = URL(url_str)

        readable = Readable(raw_html)
        navigation = Navigation(raw_html, url)

        return ScrapeResult(
            requested_url=requested_url,
            url=url.normalized,
            title=readable.title(),
            short_title=readable.short_title(),
            author=readable.author(),
            html=readable.raw_html,
            markdown=readable.md(),
            summary_html=readable.summary_html(),
            summary_md=readable.summary_md(),
            links=navigation.links,
            pagination_links=navigation.pagination_links,
        )

    async def scrape_raw(self, requested_url: str) -> tuple[str, str]:
        page = await self.browser.new_page()
        try:  # noqa: SIM105
            await page.goto(requested_url, timeout=5000, wait_until="networkidle")
        except PlaywrightError:
            pass
        raw_html = await page.content()
        await page.close()
        return page.url, raw_html

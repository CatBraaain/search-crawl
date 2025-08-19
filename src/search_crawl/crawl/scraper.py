from patchright.async_api import Browser
from patchright.async_api import Error as PlaywrightError

from ..cache_config import CacheConfig
from .parser import URL, Navigation, Readable
from .schemas import ScrapeResult


class Scraper:
    browser: Browser

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    async def scrape(
        self, requested_url: str, cache_config: CacheConfig
    ) -> ScrapeResult:
        url_str, raw_html = await self.scrape_raw_wrapper(requested_url, cache_config)
        url = URL(url_str)

        readable = Readable(raw_html)
        navigation = Navigation(raw_html, url)

        return {
            "requested_url": requested_url,
            "url": url.normalized,
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

    async def scrape_raw_wrapper(
        self, requested_url: str, cache_config: CacheConfig
    ) -> tuple[str, str]:
        scrape_with_cache = cache_config.wrap_with_cache(
            cache_key=f"scrape:{requested_url}",
            func=self.scrape_raw,
        )
        return await scrape_with_cache(requested_url)

    async def scrape_raw(self, requested_url: str) -> tuple[str, str]:
        page = await self.browser.new_page()
        try:
            await page.goto(requested_url, timeout=5000, wait_until="networkidle")
        except PlaywrightError:
            pass
        raw_html = await page.content()
        await page.close()
        return page.url, raw_html

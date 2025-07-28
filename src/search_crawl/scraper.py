from typing import TypedDict

from camoufox.async_api import Browser, BrowserContext
from cashews import cache
from markitdown import MarkItDown

from .page_parser import URL, Navigation, Readable


class ScrapeResult(TypedDict):
    requested_url: str
    url: str
    title: str
    short_title: str
    author: str
    html: str
    content: str
    summary_html: str
    summary_md: str
    links: list[str]
    pagination_links: list[str]


class Scraper:
    browser: Browser | BrowserContext
    markitdown: MarkItDown

    def __init__(
        self, browser: Browser | BrowserContext, markitdown: MarkItDown
    ) -> None:
        self.browser = browser
        self.markitdown = markitdown

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

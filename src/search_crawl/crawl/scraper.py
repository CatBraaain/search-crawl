from typing import TypedDict

from cashews import cache
from patchright.async_api import Browser

from .page_parser import URL, Navigation, Readable

cache.setup("disk://?directory=.cache&shards=0")


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
    browser: Browser

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    async def scrape(self, requested_url: str, ttl: str) -> ScrapeResult:
        url_str, raw_html = await self.scrape_raw_wrapper(requested_url, ttl)
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

    async def scrape_raw_wrapper(self, requested_url: str, ttl: str) -> tuple[str, str]:
        cached = await cache.get(requested_url)
        if cached:
            return cached
        else:
            value = await self.scrape_raw(requested_url)
            await cache.set(requested_url, value, expire=ttl)
            return value

    async def scrape_raw(self, requested_url: str) -> tuple[str, str]:
        page = await self.browser.new_page()
        await page.goto(requested_url, timeout=10000, wait_until="networkidle")
        raw_html = await page.content()
        await page.close()
        return page.url, raw_html

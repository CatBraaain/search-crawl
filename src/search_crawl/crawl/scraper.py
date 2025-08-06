from typing import TypedDict

from cashews import cache
from cashews.ttl import TTL
from patchright.async_api import Browser
from patchright.async_api import Error as PlaywrightError
from pydantic import BaseModel

from .parser import URL, Navigation, Readable

cache.setup("disk://?directory=.cache&shards=0")


class CacheConfig(BaseModel):
    readable: bool = True
    writable: bool = True
    ttl: TTL = "24h"


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

    async def scrape(
        self, requested_url: str, cache_strategy: CacheConfig
    ) -> ScrapeResult:
        url_str, raw_html = await self.scrape_raw_wrapper(requested_url, cache_strategy)
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
        self, requested_url: str, cache_strategy: CacheConfig
    ) -> tuple[str, str]:
        cached = cache_strategy.readable and await cache.get(requested_url)
        if cached:
            return cached
        else:
            value = await self.scrape_raw(requested_url)
            if cache_strategy.writable:
                await cache.set(requested_url, value, expire=cache_strategy.ttl)
            return value

    async def scrape_raw(self, requested_url: str) -> tuple[str, str]:
        page = await self.browser.new_page()
        try:
            await page.goto(requested_url, timeout=5000, wait_until="networkidle")
        except PlaywrightError:
            pass
        raw_html = await page.content()
        await page.close()
        return page.url, raw_html

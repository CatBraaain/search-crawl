import asyncio
import io
import os
import re
from typing import Any, Awaitable, Self, Sequence, TypedDict, cast
from urllib.parse import (
    parse_qsl,
    urlencode,
    urljoin,
    urlsplit,
    urlunsplit,
)

from camoufox.async_api import AsyncCamoufox, Browser, BrowserContext
from cashews import cache
from lxml import html
from markitdown import MarkItDown, StreamInfo
from readability import Document

cache.setup("disk://?directory=.cache&shards=0")


class URL:
    with_domain: str
    with_dirpath: str
    with_path: str
    with_params: str
    pagination_regex: re.Pattern

    def __init__(self, url: str) -> None:
        parsed = urlsplit(url)

        self.with_domain = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))

        dirpath = os.path.dirname(parsed.path).removesuffix("/") + "/"
        self.with_dirpath = urlunsplit((parsed.scheme, parsed.netloc, dirpath, "", ""))

        self.with_path = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))

        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        sorted_query = urlencode(sorted(query_params))
        self.with_params = urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, sorted_query, "")
        )

        pagination_pattern = r".*(p|page)[=\/]?\d+.*"
        self.pagination_regex = re.compile(
            rf"{re.escape(self.with_path)}{pagination_pattern}", re.IGNORECASE
        )

    def __str__(self) -> str:
        return self.with_params


class Readable(Document):
    markitdown: MarkItDown

    def __init__(self, raw_html: str, markitdown: MarkItDown) -> None:
        super().__init__(raw_html)
        self.markitdown = markitdown

    def content(self) -> str:
        return cast(str, super().content())

    def summary_html(self) -> str:
        return super().summary()

    def summary_md(self) -> str:
        return str(
            self.markitdown.convert_stream(
                io.BytesIO(self.summary_html().encode("utf-8")),
                stream_info=StreamInfo(mimetype="text/html", charset="utf-8"),
            )
        )


class Navigation:
    links: list[str]
    pagination_links: list[str]

    def __init__(self, html_str: str, url: URL) -> None:
        tree = html.fromstring(html_str)
        links = self.extract_links(tree, url)
        self.links = links
        self.pagination_links = [
            link for link in links if re.match(url.pagination_regex, link)
        ]

    def extract_links(self, tree: html.HtmlElement, current_url: URL) -> list[str]:
        all_links = [
            urljoin(current_url.with_dirpath, a.get("href"))
            for a in tree.cssselect("a[href]")
        ]
        inner_links = sorted(
            list(
                {
                    link
                    for link in all_links
                    if URL(link).with_domain == current_url.with_domain
                }
            )
        )
        return inner_links


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


class Crawler:
    browser: Browser | BrowserContext
    markitdown: MarkItDown
    visited: list[str]
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

        self.visited.append(requested_url)
        async with sem:
            scrape_result = await self.scrape(requested_url)
            self.results.append(scrape_result)
            await gather_with_sem(
                [
                    self.crawl(pagination_link, sem)
                    for pagination_link in scrape_result["pagination_links"]
                ],
                sem,
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
        await page.goto(requested_url, wait_until="load")
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

    async def crawl_many(self, requested_urls: list[str]) -> list[list[ScrapeResult]]:
        crawler = Crawler(self.browser, self.markitdown)
        sem = asyncio.Semaphore(2)
        return await asyncio.gather(
            *(crawler.crawl(requested_url, sem) for requested_url in requested_urls)
        )


async def gather_with_sem[T](
    coros: Sequence[Awaitable[T]], sem: asyncio.Semaphore
) -> list[T]:
    async def with_sem(sem, coro):
        async with sem:
            return await coro

    return await asyncio.gather(*(with_sem(sem, c) for c in coros))

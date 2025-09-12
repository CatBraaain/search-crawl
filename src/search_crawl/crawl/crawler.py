import asyncio

from patchright.async_api import Browser, Error as PlaywrightError

from search_crawl.cache_config import CacheConfig

from .schemas import CrawlConfig, CrawlScope, OutputFormat, ScrapeResult
from .utils import URL, Navigation, Readable


class Crawler:
    browser: Browser
    crawl_config: CrawlConfig
    cache_config: CacheConfig

    def __init__(
        self,
        browser: Browser,
        crawl_config: CrawlConfig,
        cache_config: CacheConfig,
    ) -> None:
        self.browser = browser
        self.crawl_config = crawl_config
        self.cache_config = cache_config

    async def crawl(
        self,
        requested_url: str,
        sem: asyncio.Semaphore,
    ) -> list[ScrapeResult]:
        visited: list[URL] = []
        results: list[ScrapeResult] = []

        async def _crawl(_url: str, current_depth: int = 0) -> None:
            max_pages = self.crawl_config.max_pages
            should_scrape_this = _url not in visited and (
                max_pages is None or len(visited) < max_pages
            )
            if not should_scrape_this:
                return
            visited.append(URL(_url))

            async with sem:
                result = await self.scrape(_url)
                results.append(result)

            max_depth = self.crawl_config.max_depth
            should_scrape_more = max_depth is None or current_depth < max_depth
            if not should_scrape_more:
                return

            match self.crawl_config.crawl_scope:
                case CrawlScope.PAGINATION:
                    target_links = result.pagination_links
                case CrawlScope.INTERNAL:
                    target_links = result.internal_links
                case CrawlScope.ALL:
                    target_links = result.links
                case _:
                    raise ValueError(
                        f"Invalid CrawlScope: {self.crawl_config.crawl_scope}"
                    )
            await asyncio.gather(
                *[
                    _crawl(pagination_link, current_depth + 1)
                    for pagination_link in target_links
                ]
            )

        await _crawl(requested_url)
        return results

    async def scrape(
        self,
        requested_url: str,
    ) -> ScrapeResult:
        scrape_with_cache = self.cache_config.wrap_with_cache(
            cache_key=f"scrape:{requested_url}",
            func=self.scrape_raw,
        )
        url_str, raw_html = await scrape_with_cache(requested_url)
        url = URL(url_str)

        readable = Readable(raw_html)
        navigation = Navigation(raw_html, url)

        output_format = self.crawl_config.output_format
        match output_format:
            case OutputFormat.FULL_HTML:
                content = readable.raw_html
            case OutputFormat.FULL_MARKDOWN:
                content = readable.md
            case OutputFormat.MAIN_HTML:
                content = readable.summary_html
            case OutputFormat.MAIN_MARKDOWN:
                content = readable.summary_md
            case _:
                raise ValueError(f"Invalid output format: {output_format}")

        return ScrapeResult(
            requested_url=requested_url,
            url=url.normalized,
            title=readable.title(),
            short_title=readable.short_title(),
            author=readable.author(),
            content=content,
            links=navigation.links,
            internal_links=navigation.internal_links,
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

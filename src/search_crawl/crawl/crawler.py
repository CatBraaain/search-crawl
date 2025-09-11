import asyncio

from patchright.async_api import Browser, Error as PlaywrightError

from search_crawl.cache_config import CacheConfig

from .schemas import CrawlConfig, CrawlScope, ScrapeResult
from .utils import URL, Navigation, Readable


class Crawler:
    browser: Browser

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    async def crawl(
        self,
        requested_url: str,
        sem: asyncio.Semaphore,
        crawl_config: CrawlConfig,
        cache_config: CacheConfig,
    ) -> list[ScrapeResult]:
        visited: list[URL] = []
        results: list[ScrapeResult] = []

        async def _crawl(_url: str, current_depth: int = 0) -> None:
            should_scrape_this = _url not in visited and (
                crawl_config.max_pages is None or len(visited) < crawl_config.max_pages
            )
            if not should_scrape_this:
                return
            visited.append(URL(_url))

            async with sem:
                result = await self.scrape(_url, cache_config)
                results.append(result)

            should_scrape_more = (
                crawl_config.max_depth is None or current_depth < crawl_config.max_depth
            )
            if not should_scrape_more:
                return

            match crawl_config.crawl_scope:
                case CrawlScope.PAGINATION:
                    target_links = result.pagination_links
                case CrawlScope.INTERNAL:
                    target_links = result.internal_links
                case CrawlScope.ALL:
                    target_links = result.links
                case _:
                    raise ValueError(f"Invalid CrawlScope: {crawl_config.crawl_scope}")
            await asyncio.gather(
                *[
                    _crawl(pagination_link, current_depth + 1)
                    for pagination_link in target_links
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
            markdown=readable.md,
            summary_html=readable.summary_html,
            summary_md=readable.summary_md,
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

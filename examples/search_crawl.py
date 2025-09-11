import asyncio

from search_crawl_client import (
    ApiClient,
    Configuration,
    CrawlConfig,
    CrawlRequest,
    DefaultApi,
    SearchCrawlRequest,
    SearchRequest,
)


async def main() -> None:
    config = Configuration(host="http://localhost:8000")
    async with ApiClient(config) as client:
        api = DefaultApi(client)
        res = (
            await api.search_crawl(
                SearchCrawlRequest(
                    search=SearchRequest(q="hello world", max_results=1),
                    crawl=CrawlRequest(
                        crawl_config=CrawlConfig(
                            concurrently=2,
                        )
                    ),
                )
            )
        )[0].crawl[0]

        print("URL: " + res.url)
        print("TITLE: " + res.title)
        print("MARKDOWN: ")
        print(res.summary_md[:200] + "...")


asyncio.run(main())

# ---- Output Example ----
# URL: https://en.wikipedia.org/wiki/%22Hello,_World!%22_program
# TITLE: "Hello, World!" program - Wikipedia
# MARKDOWN:
# Traditional first example of a computer programming language
# A **"Hello, World!" program** is usually a simple [computer program](/wiki/Computer_program "Computer program") that emits (or displays) t...

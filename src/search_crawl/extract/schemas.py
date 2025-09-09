import json
from typing import Any, Literal

from pydantic import BaseModel

from search_crawl.crawl.router import (
    CrawlRequest,
    CrawlRequestWithUrl,
    ScrapeResult,
)
from search_crawl.search.router import SearchRequest

InputFormat = Literal["content_markdown", "full_markdown", "content_html", "full_html"]
CrawledContent = list[list[ScrapeResult]] | list[ScrapeResult]


class ExtractRequest(BaseModel):
    model: str
    instruction: str
    json_schema: dict[str, Any]
    input_format: InputFormat = "content_markdown"

    def make_prompt(self, crawled_content: CrawledContent) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that reads information from"
                    " web pages and performs tasks based on user instructions."
                ),
            },
            {
                "role": "user",
                "content": "\n".join(
                    [
                        (
                            "Read the website contents provided in the `Content:`"
                            " section and answer the user instructions accurately."
                        ),
                        "",
                        "Instruction:",
                        self.instruction,
                        "",
                        "Contents:",
                        "```json",
                        json.dumps(self._make_content(crawled_content)),
                        "```",
                    ]
                ),
            },
        ]

    def _make_content(self, crawled_content: CrawledContent) -> list[dict[str, str]]:
        scrape_results: list[ScrapeResult] = [
            scrape_result
            for e in crawled_content
            for scrape_result in (e if isinstance(e, list) else [e])
        ]
        return [self._format_scrape_result(sr) for sr in scrape_results]

    def _format_scrape_result(self, scrape_result: ScrapeResult) -> dict[str, str]:
        match self.input_format:
            case "content_markdown":
                return scrape_result.model_dump(include={"url", "title", "summary_md"})
            case "full_markdown":
                return scrape_result.model_dump(include={"url", "title", "markdown"})
            case "content_html":
                return scrape_result.model_dump(
                    include={"url", "title", "summary_html"}
                )
            case "full_html":
                return scrape_result.model_dump(include={"url", "title", "html"})
            case _:
                raise ValueError(f"Invalid input_format: {self.input_format}")

    def make_response_format(self) -> dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {"schema": self.json_schema, "strict": True},
            "strict": True,
        }


class CrawlExtractRequest(BaseModel):
    crawl: CrawlRequestWithUrl
    extract: ExtractRequest


class SearchCrawlExtractRequest(BaseModel):
    search: SearchRequest
    crawl: CrawlRequest = CrawlRequest()
    extract: ExtractRequest

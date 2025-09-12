import json
from typing import Any

from pydantic import BaseModel

from search_crawl.crawl.router import (
    CrawlRequest,
    CrawlRequestWithUrl,
    ScrapeResult,
)
from search_crawl.search.router import SearchRequest

CrawledContent = list[list[ScrapeResult]] | list[ScrapeResult]


class ExtractRequest(BaseModel):
    model: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    instruction: str
    json_schema: dict[str, Any]

    # openapi-generator not supporting this option with optional fields
    # model_config = ConfigDict(extra="allow")

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
                        json.dumps(
                            self._make_contents(crawled_content), ensure_ascii=False
                        ),
                        "```",
                    ]
                ),
            },
        ]

    def _make_contents(self, crawled_content: CrawledContent) -> list[dict[str, str]]:
        return [
            scrape_result.model_dump(include={"url", "title", "content"})
            for e in crawled_content
            for scrape_result in (e if isinstance(e, list) else [e])
        ]

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

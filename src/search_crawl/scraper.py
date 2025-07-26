import io
import os
import re
from typing import TypedDict, cast
from urllib.parse import (
    parse_qsl,
    urlencode,
    urljoin,
    urlsplit,
    urlunsplit,
)

from lxml import html
from markitdown import MarkItDown, StreamInfo
from readability import Document


class URL:
    with_domain: str
    with_dirpath: str
    with_path: str
    normalized: str
    pagination_regex: re.Pattern

    def __init__(self, url: str) -> None:
        parsed = urlsplit(url)

        self.with_domain = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))

        dirpath = os.path.dirname(parsed.path).removesuffix("/") + "/"
        self.with_dirpath = urlunsplit((parsed.scheme, parsed.netloc, dirpath, "", ""))

        self.with_path = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))

        normalized_query = self.normalize_query(parsed.query)
        self.normalized = urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, normalized_query, "")
        )

        pagination_pattern = r".*(p|page)[=\/]?\d+.*"
        self.pagination_regex = re.compile(
            rf"{re.escape(self.with_path)}{pagination_pattern}", re.IGNORECASE
        )

    def normalize_query(self, query: str) -> str:
        query_params = parse_qsl(query, keep_blank_values=True)
        filtered = [
            (k, v)
            for k, v in query_params
            if not (k.lower() in {"p", "page"} and v == "1")
        ]
        normalized_query = urlencode(sorted(filtered))
        return normalized_query

    def __str__(self) -> str:
        return self.normalized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, URL):
            return self.normalized == other.normalized
        if isinstance(other, str):
            return self.normalized == URL(other).normalized
        return NotImplemented


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

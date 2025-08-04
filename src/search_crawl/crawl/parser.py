import io
import re
from typing import cast
from urllib.parse import urljoin

from lxml import html
from markitdown import MarkItDown, StreamInfo
from readability import Document

from .url import URL


class Readable(Document):
    def __init__(self, raw_html: str) -> None:
        super().__init__(raw_html)
        self.markitdown = MarkItDown()

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
            urljoin(current_url.normalized, a.get("href"))
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

import io
import re
from typing import cast
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
    with_basepath: str
    page: int | None
    with_path: str
    normalized: str
    pagination_regex: re.Pattern

    def __init__(self, url: str) -> None:
        parsed = urlsplit(url)

        self.with_domain = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))

        pagination_pattern = (
            r"(p|pa|pag|page|pg|paging|pagination)([-_]?num)?(=|/|-)?(?P<num>\d{1,3})"
        )
        path = parsed.path.removesuffix("/")
        basepath = re.sub(f"{pagination_pattern}$", "", path).removesuffix("/")
        self.with_basepath = urlunsplit(
            (parsed.scheme, parsed.netloc, basepath, "", "")
        )
        if matched := re.search(f"{pagination_pattern}$", url):
            self.page = int(matched.group("num"))
        else:
            self.page = None

        self.with_path = urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))

        normalized_query = self.normalize_query(parsed.query)
        self.normalized = urlunsplit(
            (parsed.scheme, parsed.netloc, path, normalized_query, "")
        )

        self.pagination_regex = re.compile(
            rf"{re.escape(self.with_basepath)}.*{pagination_pattern}.*", re.IGNORECASE
        )

    def normalize_query(self, query: str) -> str:
        query_params = parse_qsl(query, keep_blank_values=True)
        normalized_query = urlencode(sorted(query_params))
        return normalized_query

    def __str__(self) -> str:
        return self.normalized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, URL) or isinstance(other, str):
            other_url = other if isinstance(other, URL) else URL(other)
            if (
                self.page == 1
                and other_url.page is None
                and self.with_basepath == other_url.with_path
            ) or (
                other_url.page == 1
                and self.page is None
                and other_url.with_basepath == self.with_path
            ):
                return True
            else:
                return self.normalized == other_url.normalized

        return NotImplemented


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

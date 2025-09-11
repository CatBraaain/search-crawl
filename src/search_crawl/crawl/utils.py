import io
import re
from typing import Self
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


class PaginationPattern:
    text = r"(p|pa|pag|page|pg|paging|pagination)([-_]?num)?"
    num = r"(?P<num>\d{1,3})"
    path = rf"[/-_]{text}[/-]?{num}$"
    param = rf"(^|&){text}[=]{num}"


class URL:
    with_domain: str
    with_path: str
    with_pagination_base: str
    page: int | None
    normalized: str

    def __init__(self, url: str) -> None:
        parsed = urlsplit(url)
        path = parsed.path.removesuffix("/")

        self.with_domain = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
        self.with_path = urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))

        pagination_basepath = re.sub(PaginationPattern.path, "", path)
        self.with_pagination_base = urlunsplit(
            (parsed.scheme, parsed.netloc, pagination_basepath, "", "")
        )

        matched = re.search(PaginationPattern.param, parsed.query) or re.search(
            PaginationPattern.path, path
        )
        if matched:
            self.page = int(matched.group("num"))
        else:
            self.page = None

        normalized_query = self.normalize_query(parsed.query)
        self.normalized = urlunsplit(
            (parsed.scheme, parsed.netloc, path, normalized_query, "")
        )

    def normalize_query(self, query: str) -> str:
        query_params = parse_qsl(query, keep_blank_values=True)
        normalized_query = urlencode(sorted(query_params))
        return normalized_query

    def __eq__(self, other: object) -> bool:
        if isinstance(other, URL | str):
            other_url = other if isinstance(other, URL) else URL(other)
            if (
                self.page == 1
                and other_url.page is None
                and self.with_pagination_base == other_url.with_path
            ) or (
                other_url.page == 1
                and self.page is None
                and other_url.with_pagination_base == self.with_path
            ):
                return True
            else:
                return self.normalized == other_url.normalized

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.normalized)

    def is_pagination_of(self, other: Self) -> bool:
        return (
            self.with_pagination_base == other.with_pagination_base
            and self.page is not None
        )


class Readable(Document):
    raw_html: str
    markitdown: MarkItDown

    def __init__(self, raw_html: str) -> None:
        super().__init__(raw_html)
        self.raw_html = raw_html
        self.markitdown = MarkItDown()

    @property
    def md(self) -> str:
        try:
            return str(
                self.markitdown.convert_stream(
                    io.BytesIO(self.raw_html.encode("utf-8")),
                    stream_info=StreamInfo(mimetype="text/html", charset="utf-8"),
                )
            )
        except Exception:
            return ""

    @property
    def summary_html(self) -> str:
        try:
            return super().summary()
        except Exception:
            return ""

    @property
    def summary_md(self) -> str:
        try:
            return str(
                self.markitdown.convert_stream(
                    io.BytesIO(self.summary_html.encode("utf-8")),
                    stream_info=StreamInfo(mimetype="text/html", charset="utf-8"),
                )
            )
        except Exception:
            return ""


class Navigation:
    links: list[str]
    internal_links: list[str]
    pagination_links: list[str]

    def __init__(self, html_str: str, url: URL) -> None:
        self.links = (
            sorted(
                [
                    urljoin(url.normalized, a.get("href"))
                    for a in html.fromstring(html_str).cssselect("a[href]")
                ]
            )
            if html_str
            else []
        )
        self.internal_links = [
            link for link in self.links if URL(link).with_domain == url.with_domain
        ]
        self.pagination_links = [
            link for link in self.internal_links if URL(link).is_pagination_of(url)
        ]

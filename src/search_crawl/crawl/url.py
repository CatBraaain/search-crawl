import re
from typing import Self
from urllib.parse import (
    parse_qsl,
    urlencode,
    urlsplit,
    urlunsplit,
)


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
        if isinstance(other, URL) or isinstance(other, str):
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

    def is_pagination_of(self, other: Self) -> bool:
        return (
            self.with_pagination_base == other.with_pagination_base
            and self.page is not None
        )

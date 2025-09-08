import pytest

from search_crawl.crawl.utils import URL


def test_with_domain() -> None:
    assert URL("https://example.com/path/page/2").with_domain == "https://example.com"
    assert URL("http://test.com/a/b/c").with_domain == "http://test.com"
    assert (
        URL("https://web-scraping.dev/products?page=2").with_domain
        == "https://web-scraping.dev"
    )
    assert URL("https://web-scraping.dev/").with_domain == "https://web-scraping.dev"
    assert URL("https://web-scraping.dev").with_domain == "https://web-scraping.dev"


def test_with_basepath() -> None:
    example_path = "https://example.com"
    assert URL(f"{example_path}").with_pagination_base == example_path
    assert URL(f"{example_path}/").with_pagination_base == example_path
    assert URL(f"{example_path}/a").with_pagination_base == example_path + "/a"
    assert URL(f"{example_path}/a/").with_pagination_base == example_path + "/a"

    assert URL(f"{example_path}?p=2").with_pagination_base == example_path
    assert URL(f"{example_path}?pa=2").with_pagination_base == example_path
    assert URL(f"{example_path}?pag=2").with_pagination_base == example_path
    assert URL(f"{example_path}?page=2").with_pagination_base == example_path
    assert URL(f"{example_path}?pg=2").with_pagination_base == example_path
    assert URL(f"{example_path}?paging=2").with_pagination_base == example_path
    assert URL(f"{example_path}?pagination=2").with_pagination_base == example_path
    assert URL(f"{example_path}?pagenum=2").with_pagination_base == example_path
    assert URL(f"{example_path}?p-num=2").with_pagination_base == example_path
    assert URL(f"{example_path}?page-num=2").with_pagination_base == example_path
    assert URL(f"{example_path}/p/2").with_pagination_base == example_path
    assert URL(f"{example_path}/page/2").with_pagination_base == example_path
    assert URL(f"{example_path}/page-num/2").with_pagination_base == example_path
    assert URL(f"{example_path}/p2").with_pagination_base == example_path
    assert URL(f"{example_path}/p-2").with_pagination_base == example_path
    assert URL(f"{example_path}/p-num-2").with_pagination_base == example_path
    assert URL(f"{example_path}/page-num-2").with_pagination_base == example_path
    assert URL(f"{example_path}/a/b?p=2").with_pagination_base == example_path + "/a/b"
    assert URL(f"{example_path}/a/b/p/2").with_pagination_base == example_path + "/a/b"


def test_with_path() -> None:
    example_path = "https://example.com"
    assert URL(f"{example_path}/a/b").with_path == f"{example_path}/a/b"
    assert URL(f"{example_path}/a/b/").with_path == f"{example_path}/a/b"
    assert URL(f"{example_path}/a/b?p=2").with_path == f"{example_path}/a/b"
    assert URL(f"{example_path}/a/b/?p=2").with_path == f"{example_path}/a/b"


def test_normalized() -> None:
    example_path = "https://example.com"
    assert URL(f"{example_path}?p=2").normalized == f"{example_path}?p=2"
    assert URL(f"{example_path}?page=2").normalized == f"{example_path}?page=2"
    assert URL(f"{example_path}?z=9&b=2").normalized == f"{example_path}?b=2&z=9"


@pytest.mark.parametrize("page_num", range(1, 4), ids=lambda x: f"page_num={x}")
def test_pagination(page_num: int) -> None:
    example_path = "https://example.com"
    assert URL(f"{example_path}").page is None
    assert URL(f"{example_path}/").page is None
    assert URL(f"{example_path}?p={page_num}").page == page_num
    assert URL(f"{example_path}?pa={page_num}").page == page_num
    assert URL(f"{example_path}?pag={page_num}").page == page_num
    assert URL(f"{example_path}?page={page_num}").page == page_num
    assert URL(f"{example_path}?pg={page_num}").page == page_num
    assert URL(f"{example_path}?paging={page_num}").page == page_num
    assert URL(f"{example_path}?pagination={page_num}").page == page_num
    assert URL(f"{example_path}?pagenum={page_num}").page == page_num
    assert URL(f"{example_path}?p-num={page_num}").page == page_num
    assert URL(f"{example_path}?page-num={page_num}").page == page_num
    assert URL(f"{example_path}/p/{page_num}").page == page_num
    assert URL(f"{example_path}/page/{page_num}").page == page_num
    assert URL(f"{example_path}/page-num/{page_num}").page == page_num
    assert URL(f"{example_path}/p{page_num}").page == page_num
    assert URL(f"{example_path}/p-{page_num}").page == page_num
    assert URL(f"{example_path}/p-num-{page_num}").page == page_num
    assert URL(f"{example_path}/page-num-{page_num}").page == page_num
    assert URL(f"{example_path}/a/b?p={page_num}").page == page_num
    assert URL(f"{example_path}/a/b/p/{page_num}").page == page_num


def test_page1_equals_toppage() -> None:
    assert URL("https://example.com/a?page=1") == URL("https://example.com/a")
    assert URL("https://example.com/a?page=1") == "https://example.com/a"
    assert URL("https://example.com/a?p=1") == URL("https://example.com/a")
    assert URL("https://example.com/a?p=1") == "https://example.com/a"


def test_page2_not_equals_toppage() -> None:
    assert URL("https://example.com/a?page=2") != URL("https://example.com/a")
    assert URL("https://example.com/a?page=2") != "https://example.com/a"
    assert URL("https://example.com/a?p=2") != URL("https://example.com/a")
    assert URL("https://example.com/a?p=2") != "https://example.com/a"


def test_sorted_params_equals_unsorted_params() -> None:
    assert URL("https://example.com/a?a=1&b=1") == URL("https://example.com/a?b=1&a=1")
    assert URL("https://example.com/a?a=1&b=1") == "https://example.com/a?b=1&a=1"


def test_with_slash_equals_without_slash() -> None:
    assert URL("https://example.com/a?page=1") == "https://example.com/a/?page=1"
    assert URL("https://example.com/a?page=1") == URL("https://example.com/a/?page=1")

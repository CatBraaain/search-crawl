import pytest

from search_crawl.crawl.utils import URL


@pytest.fixture
def example_url() -> str:
    return "https://example.com"


def test_with_domain(example_url: str) -> None:
    assert URL(f"{example_url}").with_domain == example_url
    assert URL(f"{example_url}/").with_domain == example_url
    assert URL(f"{example_url}/a/b/c").with_domain == example_url
    assert URL(f"{example_url}/path/page/2").with_domain == example_url
    assert URL(f"{example_url}/products?page=2").with_domain == example_url


def test_with_pagination_base(example_url: str) -> None:
    assert URL(f"{example_url}").with_pagination_base == example_url
    assert URL(f"{example_url}/").with_pagination_base == example_url
    assert URL(f"{example_url}/a").with_pagination_base == example_url + "/a"
    assert URL(f"{example_url}/a/").with_pagination_base == example_url + "/a"

    i = 2
    assert URL(f"{example_url}?p={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?pa={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?pag={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?page={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?pg={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?paging={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?pagination={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?pagenum={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?p-num={i}").with_pagination_base == example_url
    assert URL(f"{example_url}?page-num={i}").with_pagination_base == example_url
    assert URL(f"{example_url}/p/{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/page/{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/page-num/{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/p{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/p-{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/p-num-{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/page-num-{i}").with_pagination_base == example_url
    assert URL(f"{example_url}/a/b?p={i}").with_pagination_base == example_url + "/a/b"
    assert URL(f"{example_url}/a/b/p/{i}").with_pagination_base == example_url + "/a/b"


def test_with_path(example_url: str) -> None:
    assert URL(f"{example_url}/a/b").with_path == f"{example_url}/a/b"
    assert URL(f"{example_url}/a/b/").with_path == f"{example_url}/a/b"
    assert URL(f"{example_url}/a/b?p=2").with_path == f"{example_url}/a/b"
    assert URL(f"{example_url}/a/b/?p=2").with_path == f"{example_url}/a/b"


def test_normalized(example_url: str) -> None:
    assert URL(f"{example_url}?p=2").normalized == f"{example_url}?p=2"
    assert URL(f"{example_url}?page=2").normalized == f"{example_url}?page=2"
    assert URL(f"{example_url}?z=9&b=2").normalized == f"{example_url}?b=2&z=9"


@pytest.mark.parametrize("page_num", [1, 3, 5], ids=lambda x: f"page_num={x}")
def test_pagination(example_url: str, page_num: int) -> None:
    assert URL(f"{example_url}").page is None
    assert URL(f"{example_url}/").page is None
    assert URL(f"{example_url}?p={page_num}").page == page_num
    assert URL(f"{example_url}?pa={page_num}").page == page_num
    assert URL(f"{example_url}?pag={page_num}").page == page_num
    assert URL(f"{example_url}?page={page_num}").page == page_num
    assert URL(f"{example_url}?pg={page_num}").page == page_num
    assert URL(f"{example_url}?paging={page_num}").page == page_num
    assert URL(f"{example_url}?pagination={page_num}").page == page_num
    assert URL(f"{example_url}?pagenum={page_num}").page == page_num
    assert URL(f"{example_url}?p-num={page_num}").page == page_num
    assert URL(f"{example_url}?page-num={page_num}").page == page_num
    assert URL(f"{example_url}/p/{page_num}").page == page_num
    assert URL(f"{example_url}/page/{page_num}").page == page_num
    assert URL(f"{example_url}/page-num/{page_num}").page == page_num
    assert URL(f"{example_url}/p{page_num}").page == page_num
    assert URL(f"{example_url}/p-{page_num}").page == page_num
    assert URL(f"{example_url}/p-num-{page_num}").page == page_num
    assert URL(f"{example_url}/page-num-{page_num}").page == page_num
    assert URL(f"{example_url}/a/b?p={page_num}").page == page_num
    assert URL(f"{example_url}/a/b/p/{page_num}").page == page_num


def test_page1_equals_toppage(example_url: str) -> None:
    assert URL(f"{example_url}/a?page=1") == URL(f"{example_url}/a")
    assert URL(f"{example_url}/a?page=1") == f"{example_url}/a"
    assert URL(f"{example_url}/a?p=1") == URL(f"{example_url}/a")
    assert URL(f"{example_url}/a?p=1") == f"{example_url}/a"


def test_page2_not_equals_toppage(example_url: str) -> None:
    assert URL(f"{example_url}/a?page=2") != URL("{example_url}/a")
    assert URL(f"{example_url}/a?page=2") != "{example_url}/a"
    assert URL(f"{example_url}/a?p=2") != URL("{example_url}/a")
    assert URL(f"{example_url}/a?p=2") != "{example_url}/a"


def test_sorted_params_equals_unsorted_params(example_url: str) -> None:
    assert URL(f"{example_url}/a?a=1&b=1") == URL(f"{example_url}/a?b=1&a=1")
    assert URL(f"{example_url}/a?a=1&b=1") == f"{example_url}/a?b=1&a=1"


def test_with_slash_equals_without_slash(example_url: str) -> None:
    assert URL(f"{example_url}/a?page=1") == URL(f"{example_url}/a/?page=1")
    assert URL(f"{example_url}/a?page=1") == f"{example_url}/a/?page=1"

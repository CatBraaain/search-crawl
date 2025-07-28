import pytest

from search_crawl.scraper import URL


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
    assert URL(f"{example_path}").with_basepath == example_path
    assert URL(f"{example_path}/").with_basepath == example_path
    assert URL(f"{example_path}/a").with_basepath == example_path + "/a"
    assert URL(f"{example_path}/a/").with_basepath == example_path + "/a"

    assert URL(f"{example_path}?p=2").with_basepath == example_path
    assert URL(f"{example_path}?pa=2").with_basepath == example_path
    assert URL(f"{example_path}?pag=2").with_basepath == example_path
    assert URL(f"{example_path}?page=2").with_basepath == example_path
    assert URL(f"{example_path}?pg=2").with_basepath == example_path
    assert URL(f"{example_path}?paging=2").with_basepath == example_path
    assert URL(f"{example_path}?pagination=2").with_basepath == example_path
    assert URL(f"{example_path}?pagenum=2").with_basepath == example_path
    assert URL(f"{example_path}?p-num=2").with_basepath == example_path
    assert URL(f"{example_path}?page-num=2").with_basepath == example_path
    assert URL(f"{example_path}/p/2").with_basepath == example_path
    assert URL(f"{example_path}/page/2").with_basepath == example_path
    assert URL(f"{example_path}/page-num/2").with_basepath == example_path
    assert URL(f"{example_path}/p2").with_basepath == example_path
    assert URL(f"{example_path}/p-2").with_basepath == example_path
    assert URL(f"{example_path}/p-num-2").with_basepath == example_path
    assert URL(f"{example_path}/page-num-2").with_basepath == example_path
    assert URL(f"{example_path}/a/b?p=2").with_basepath == example_path + "/a/b"
    assert URL(f"{example_path}/a/b/p/2").with_basepath == example_path + "/a/b"


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


def test_pagination() -> None:
    example_path = "https://example.com"
    assert URL(f"{example_path}").page is None
    assert URL(f"{example_path}/").page is None
    assert URL(f"{example_path}?p=2").page == 2
    assert URL(f"{example_path}?pa=3").page == 3
    assert URL(f"{example_path}?pag=4").page == 4
    assert URL(f"{example_path}?page=5").page == 5
    assert URL(f"{example_path}?pg=2").page == 2
    assert URL(f"{example_path}?paging=2").page == 2
    assert URL(f"{example_path}?pagination=2").page == 2
    assert URL(f"{example_path}?pagenum=2").page == 2
    assert URL(f"{example_path}?p-num=2").page == 2
    assert URL(f"{example_path}?page-num=2").page == 2
    assert URL(f"{example_path}/p/2").page == 2
    assert URL(f"{example_path}/page/3").page == 3
    assert URL(f"{example_path}/page-num/4").page == 4
    assert URL(f"{example_path}/p2").page == 2
    assert URL(f"{example_path}/p-2").page == 2
    assert URL(f"{example_path}/p-num-2").page == 2
    assert URL(f"{example_path}/page-num-2").page == 2
    assert URL(f"{example_path}/a/b?p=2").page == 2
    assert URL(f"{example_path}/a/b/p/2").page == 2


def test_equality() -> None:
    assert URL("https://example.com/a?page=1") == URL("https://example.com/a")
    assert URL("https://example.com/a?page=1") == "https://example.com/a"
    assert URL("https://example.com/a?a=1&b=1") == "https://example.com/a?b=1&a=1"
    assert URL("https://example.com/a?p=1") == "https://example.com/a"
    assert URL("https://example.com/a?p=2") != "https://example.com/a"
    assert URL("https://example.com/a?page=1") == URL("https://example.com/a/?page=1")

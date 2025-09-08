from pydantic import BaseModel

from search_crawl_client import (
    CacheConfig,
    CrawlExtractRequest,
    CrawlRequest,
    CrawlRequestWithUrl,
    DefaultApi,
    ExtractRequest,
    SearchCrawlExtractRequest,
    SearchRequest,
)


class Country(BaseModel):
    """
    Country information model following the format of
    https://www.scrapethissite.com/pages/simple/
    """

    country_name: str
    capital: str
    population: int
    area: float

    class Config:
        title = "Country"


async def test_crawl_extract(api: DefaultApi):
    res = await api.crawl_extract(
        CrawlExtractRequest(
            crawl=CrawlRequestWithUrl(
                url="https://www.scrapethissite.com/pages/simple/",
                cache_config=CacheConfig(readable=False, writable=True),
            ),
            extract=ExtractRequest(
                model="gemini/gemini-2.0-flash-lite",
                instruction="which one has the biggest population",
                json_schema=Country.model_json_schema(),
                input_format="full_markdown",
            ),
        )
    )

    assert res == {
        "country_name": "China",
        "capital": "Beijing",
        "population": 1330044000,
        "area": 9596960.0,
    }


async def test_search_crawl_extract(api: DefaultApi):
    res = await api.search_crawl_extract(
        SearchCrawlExtractRequest(
            search=SearchRequest(
                q="China wikipedia",
                max_results=1,
                cache_config=CacheConfig(readable=False, writable=True),
            ),
            crawl=CrawlRequest(),
            extract=ExtractRequest(
                model="gemini/gemini-2.0-flash-lite",
                instruction=("How many populations are there in China?"),
                json_schema=Country.model_json_schema(),
            ),
        )
    )
    country = Country.model_validate(res)
    assert country.population > 1330044000
